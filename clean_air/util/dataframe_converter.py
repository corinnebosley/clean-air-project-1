"""
This module contains functions to convert between dataframe types.
"""

from clean_air.util.cubes import get_xy_coords
from iris.pandas import _assert_shared, _as_pandas_coord, as_data_frame
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import warnings


def as_pandas_data(data, copy=True):
    """
    Sort iris cube style data into pandas style data.
    :param data: Data array to be converted.
    :param copy: Boolean value representing whether the data should be copied.
    or not (this will return an error if the array is masked).
    :return: Data array in pandas format.
    """
    if isinstance(data, np.ma.MaskedArray):
        if not copy:
            raise ValueError("Masked arrays must always be copied.")
        data = data.astype('f').filled(np.nan)
    elif copy:
        data = data.copy()

    return data


def as_series(cube, index=None, copy=True):
    """
    Static function to convert an iris cube into a pandas series.

    :param cube: iris cube (1-dimensional) for conversion.
    :param index: 1-dimensional array representing the order of data for input
    (if not supplied, the input order will be the same as the cube data).
    :param copy: boolean value representing whether to keep a copy of the
    data upon conversion.
    :return: pandas Series containing information converted from iris cube.
    """
    # NOTE: This is not yet used in this converter, but it will be needed soon.
    # It is as yet untested and unfinished; pulled from iris but in need of
    # simplification and modification.
    data = as_pandas_data(cube.data)
    if not index:
        if cube.dim_coords:
            index = _as_pandas_coord(cube.dim_coords[0])
    else:
        index = _as_pandas_coord(index)

    series = pd.Series(data, index)
    if not copy:
        _assert_shared(data, series)

    return series


def _make_geo(cube, x_coord, y_coord):
    """
    Helper function for conversion to geodataframe(s)
    :param cube: cube for conversion
    :param x_coord: iris dim coord representing x direction
    :param y_coord: iris dim coord representing y direction
    :return: list of geodataframes
    """
    dataframes = []
    for sub_cube in cube.slices([x_coord, y_coord], ordered=True):
        # Get the coordinates, data and geometry in the right
        # order here:
        x_coords_pd = []
        y_coords_pd = []
        data_pd = []
        geom = []
        i = 0
        for x in x_coord.points:
            # Reset the y-coord index to 0 each time we loop over the x-coord:
            j = 0
            for y in y_coord.points:
                x_coords_pd.append(x)
                y_coords_pd.append(y)
                data_pd.append(sub_cube.data[i, j])
                geom.append(Point(x, y))
                # i and j represent the index values of the coords, so
                # they need to stop counting at the end of the coord arrays.
                if j < len(y_coord.points) - 1:
                    j += 1
            if i < len(x_coord.points) - 1:
                i += 1

        # Now construct pandas dataframe object for this sub_cube:
        pandas_df = pd.DataFrame({'x_coord': x_coords_pd,
                                  'y_coord': y_coords_pd,
                                  'data': data_pd})

        # Then make geometry in correct form (which is a list of
        # shapely.geometry.Points objects) and convert to GeoDataFrame:
        geo_df = GeoDataFrame(pandas_df, geometry=geom)
        dataframes.append(geo_df)

    return dataframes


def convert_to_geodf(cube, restitch=True):
    """
    Callable for converting iris-style cubes into geopandas dataframes.

    Note: This conversion is only possible for 2-dimensional cubes, so input
    cubes with more than two dimensions will be sliced up before conversion
    and then restitched if necessary.  Cubes with less than two dimensions
    will be converted to a series instead.

    :param cube: input cube.
    :param restitch: Boolean representing whether to concatenate the
    dataframes after conversion to pandas arrays.
    :return: pandas-style dataframe(s) or series, depending on input (see note).
    """
    geodataframes = series = geodataframe = None
    if len(cube.dim_coords) == 2:
        restitch = False

    # For cubes with more than two dim coords:
    if len(cube.dim_coords) >= 2:
        x_coord, y_coord = get_xy_coords(cube)
        # If there are more than two coords, we need to look for standard
        # xy dimension coords and use them to slice the cube up:
        geodataframes = _make_geo(cube, x_coord, y_coord)

        # Now we have a set of 2D geopandas dataframes which must be
        # stitched back together if required
        if restitch:
            geodataframe = pd.concat(geodataframes)

    # For cubes with less than 2 dim coords (warn then convert to series):
    elif len(cube.dim_coords) < 2:
        warnings.warn("Converting to non-geographical series instead of "
                      "geodataframe as there is only one coordinate.")
        series = as_series(cube)

    if len(cube.dim_coords) >= 2:
        if restitch is True:
            return geodataframe
        else:
            return geodataframes
    elif len(cube.dim_coords) < 2:
        return series

