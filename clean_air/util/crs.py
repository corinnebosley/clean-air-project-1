"""
Helper functions for dealing with coordinate reference systems.
"""

import warnings

import numpy as np
import cartopy.crs as ccrs
import pyproj
import shapely.ops

# Cartopy classes corresponding to EPSG codes
_CARTOPY_EPSG = {
    4326: (ccrs.Geodetic, {}),
    23032: (ccrs.EuroPP, {}),
    27700: (ccrs.OSGB, {"approx": False}),
    29902: (ccrs.OSNI, {"approx": False}),
}

# Map of proj4 projection names to appropriate classes
# Expected parameters have been noted for reference only, there's no need to
# manually validate these
_CARTOPY_CLASSES = {
    # no arguments
    "lonlat": ccrs.Geodetic,

    # lon_0
    "eqc": ccrs.PlateCarree,
    "cea": ccrs.LambertCylindrical,
    "igh": ccrs.InterruptedGoodeHomolosine,
    "mill": ccrs.Miller,  # note: spheres only

    # lon_0, lat_0
    "ortho": ccrs.Orthographic,
    "gnom": ccrs.Gnomonic,  # note: spheres only

    # lon_0, x_0, y_0
    "eck1": ccrs.EckertI,
    "eck2": ccrs.EckertII,
    "eck3": ccrs.EckertIII,
    "eck4": ccrs.EckertIV,
    "eck5": ccrs.EckertV,
    "eck6": ccrs.EckertVI,
    "eqearth": ccrs.EqualEarth,
    "moll": ccrs.Mollweide,
    "robin": ccrs.Robinson,
    "sinu": ccrs.Sinusoidal,
    "stere": ccrs.Stereographic,

    # lon_0, lat_0, x_0, y_0
    "laea": ccrs.LambertAzimuthalEqualArea,
    "aeqd": ccrs.AzimuthalEquidistant,

    # lon_0, lat_0, x_0, y_0, lat_1, lat_2
    "lcc": ccrs.LambertConformal,
    "aea": ccrs.AlbersEqualArea,
    "eqdc": ccrs.EquidistantConic,

    # The following all set units = "m", which we may want to verify is true

    # lon_0, x_0, y_0, lat_ts, k_0
    "merc": ccrs.Mercator,
    # Note: also takes a min_latitude and max_latitude, used to determine its
    # boundary

    # lon_0, lat_0, k, x_0, y_0
    "tmerc": ccrs.TransverseMercator,

    # zone, south
    "utm": ccrs.UTM,

    # lon_0, lat_0, h, x_0, y_0
    "geos": ccrs.Geostationary,
    "nsper": ccrs.NearsidePerspective,
}

# Map of proj4 names to keyword arguments for a cartopy Globe
_GLOBE_PARAMS = {
    "datum": "datum",
    "ellps": "ellipse",
    "a": "semimajor_axis",
    "b": "semiminor_axis",
    "f": "flattening",
    "rf": "inverse_flattening",
    "towgs84": "towgs84",
    "nadgrids": "nadgrids",
}

# Map of proj4 names to keyword arguments for a cartopy CRS
_CRS_PARAMS = {
    "lon_0": "central_longitude",  # Except rotated geodetic
    "lat_0": "central_latitude",
    "x_0": "false_easting",
    "y_0": "false_northing",
    "k": "scale_factor",
    "k_0": "scale_factor",
    "lat_ts": "latitude_true_scale",
    "h": "satellite_height",
    "south": "southern_hemisphere",

    # We'll use names like "[foo]" to indicate that the value of "foo" must
    # be an array, which all values will be appended to
    "lat_1": "[standard_parallels]",
    "lat_2": "[standard_parallels]",

    # Will only be used for rotated geodetic
    "o_lon_p": "central_rotated_longitude",
    "o_lat_p": "pole_latitude",
}

# Ignore the warning from pyproj that converting to a proj4 string loses
# information
warnings.filterwarnings(
    "ignore",
    "You will likely lose important projection information",
)


def as_pyproj_crs(crs):
    """
    Represent a cartopy CRS as a pyproj CRS.
    """
    if isinstance(crs, pyproj.CRS):
        return crs

    if isinstance(crs, ccrs.CRS):
        # Conveniently, Cartopy exposes a proj4 init string, which pyproj
        # can handle
        return pyproj.CRS(crs.proj4_init)

    raise TypeError(f"Unrecognised CRS: {crs}")


def as_cartopy_crs(crs):
    """
    Represent a pyproj CRS as a cartopy CRS.
    """
    if isinstance(crs, ccrs.CRS):
        return crs

    if not isinstance(crs, pyproj.CRS):
        raise TypeError(f"Unrecognised CRS: {crs}")

    # Check EPSG code to use specific cartopy classes where possible.
    # Minor note of caution: this method (by default) finds a "close enough"
    # EPSG code, with a confidence level of 70%. Apparently this is useful
    # because "trivial" differences like listing the axes in a different order,
    # or missing names, are taken into account.
    epsg = crs.to_epsg()
    if epsg in _CARTOPY_EPSG:
        constructor, args = _CARTOPY_EPSG[epsg]
        return constructor(**args)

    # Otherwise, we have the tedious task of converting proj4 parameters to
    # a cartopy class + parameters + globe parameters
    constructor = None
    crs_params = {}
    globe_params = {}

    # First need proj4 params, as a dict instead of an actual proj4 string
    params = crs.to_dict()

    # Determine the projection
    proj_name = params.pop("proj")
    if proj_name in _CARTOPY_CLASSES:
        constructor = _CARTOPY_CLASSES[proj_name]
    elif proj_name == "ob_tran" and params.pop("o_proj") == "latlon":
        # Check for rotated pole as a special case
        constructor = ccrs.RotatedGeodetic
        crs_params["pole_longitude"] = params.pop("lon_0") - 180

    if constructor is None:
        raise ValueError(f"Cannot handle projection '{proj_name}'")

    # Special handling for spheres
    r = params.pop("R", None)
    if r is not None:
        params["a"] = params["b"] = r

    # Split the parameters into those for the globe and those for the crs
    # Note: the sorting is specifically to guarantee that we handle lat_1
    # before lat_2, because they need to be put into an array in that order
    unrecognised = []
    for key, val in sorted(params.items()):
        # Handle "flags" - parameters that have no meaningful "value" so
        # were given a value of None
        if key == "south":
            val = True

        if key in _GLOBE_PARAMS:
            globe_params[_GLOBE_PARAMS[key]] = val
        elif key in _CRS_PARAMS:
            name = _CRS_PARAMS[key]
            if name.startswith("["):
                # Force into an array if needed
                name = name.strip("[]")
                crs_params.setdefault(name, []).append(val)
            else:
                crs_params[name] = val
        elif key not in ("no_defs", "wktext", "type", "units", "to_meter"):
            unrecognised.append((key, val))

    if unrecognised:
        warnings.warn(f"Some parameters were not handled: {unrecognised}")

    # Special handling for scale factors
    # Cartopy refuses to accept both "scale_factor" and "latitude_true_scale",
    # even if they match the defaults that proj4 defines.  Try to avoid it
    # raising this error by removing these defaults.
    if crs_params.get("latitude_true_scale") == 0:
        crs_params.pop("latitude_true_scale")
    if crs_params.get("scale_factor") == 1:
        crs_params.pop("scale_factor")

    return constructor(**crs_params, globe=ccrs.Globe(**globe_params))


def _transformer_cartopy(source, target):
    def transform(xs, ys):
        tfpoints = target.transform_points(source, np.array(xs), np.array(ys))
        # Cartopy gave us an array of shape (n, 3), but shapely expects output
        # of the same type as the input, ie two lists of length n.
        # A numpy array of shape (2, n) counts as two lists, so just need to
        # drop the z coordinates and transpose.
        return tfpoints[:, 0:2].T

    return transform

def _transformer_pyproj(source, target):
    transformer = pyproj.Transformer.from_crs(source, target, always_xy=True)
    return transformer.transform

def transform_shape(shape, source, target):
    # Determine an appropriate transformation function based on type
    # If the CRSs are not compatible types, assume it is slightly more helpful
    # to match the target, so convert the source
    if isinstance(source, ccrs.CRS):
        if isinstance(target, ccrs.CRS):
            transformer = _transformer_cartopy(source, target)
        else:
            source = as_pyproj_crs(source)
            transformer = _transformer_pyproj(source, target)
    else:
        if isinstance(target, ccrs.CRS):
            source = as_cartopy_crs(source)
            transformer = _transformer_cartopy(source, target)
        else:
            transformer = _transformer_pyproj(source, target)

    return shapely.ops.transform(transformer, shape)
