"""
Unit tests for the util.crs submodule
"""

import cartopy.crs as ccrs
import pyproj
import pytest

from clean_air import util

cases = [
    (pyproj.CRS.from_epsg(4326), ccrs.Geodetic()),
    (pyproj.CRS.from_epsg(27700), ccrs.OSGB()),
    (pyproj.CRS.from_epsg(3857), ccrs.Mercator.GOOGLE),

    (
        pyproj.CRS.from_epsg(3057),
        ccrs.LambertConformal(
            -19, 65,
            false_easting=500_000,
            false_northing=500_000,
            standard_parallels=(64.25, 65.75),
        )
    ),

    (
        # Not sure how else to define this case other than copying what
        # our cartopy -> pyproj converter does...
        pyproj.CRS.from_epsg(
            """
            +ellps=WGS84 +a=6371229 +b=6371229
            +proj=ob_tran +o_proj=latlon +o_lon_p=0.0 +o_lat_p=177.5
            +lon_0=217.5
            +to_meter=0.0174532925199433 +no_defs
            """
        ),
        ccrs.RotatedGeodetic(
            37.5, 177.5,
            globe=ccrs.Globe(semimajor_axis=6371229, semiminor_axis=6371229),
        )
    ),
]

@pytest.mark.parametrize("source, target", cases)
def test_as_cartopy(source, target):
    converted = util.crs.as_cartopy_crs(source)
    # Cartopy implements equality by comparing proj4 strings, which may
    # fail due to differences such as the order of parameters, or whether a
    # number ends with ".0" or not.  Instead, compare the underlying dicts.
    assert converted.proj4_params == target.proj4_params

# Note that we can reuse the same cases, but labeled the other way round
@pytest.mark.parametrize("target, source", cases)
def test_as_pyproj(source, target):
    converted = util.crs.as_pyproj_crs(source)
    # Pyproj also needs to be told to ignore ordering, instead of using
    # the equality operator
    assert converted.equals(target, ignore_axis_order=True)
