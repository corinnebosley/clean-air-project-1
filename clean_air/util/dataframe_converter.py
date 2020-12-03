"""
This module contains functions to convert between dataframe types.
"""

from clean_air.util.cubes import get_xy_coords
from iris.util import guess_coord_axis
from iris.pandas import _assert_shared, _as_pandas_coord, as_data_frame
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point


def as_pandas_data(data, copy=True):
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


class CubeToDataframe:
    """
    Class to convert iris-type cubes to pandas-type dataframes.
    """
    def __init__(self, cube):
        self.cube = cube
        self.dims = cube.dim_coords
        # TODO: modify this to use Barnaby's method of getting xy coords,
        #  which is much shorter and quicker.
        for coord in self.cube.coords():
            axis = guess_coord_axis(coord)
            if axis == 'X':
                self.x_coord = coord
            elif axis == 'Y':
                self.y_coord = coord

    def convert_to_geodf(self, restitch=True):
        # Iris function iris.pandas.as_data_frame will only convert a
        # 2D cube into a dataframe, so first make sure all data for conversion
        # is sliced into 2D slices:

        if len(self.dims) > 2:
            # If there are more than two coords, we need to look for standard
            # xy dimension coords and use them to slice the cube up:
            dataframes = []
            for sub_cube in self.cube.slices([self.x_coord, self.y_coord]):
                # Get the coordinates, data and geometry in the right
                # order here:
                self.x_coords_pd = []
                self.y_coords_pd = []
                self.data_pd = []
                self.geom = []
                i = j = 0
                for x in self.x_coord.points:
                    for y in self.y_coord.points:
                        self.x_coords_pd.append(x)
                        self.y_coords_pd.append(y)
                        # TODO: Handle masked data somehow?
                        #  (identify with fill_value if need be)
                        self.data_pd.append(sub_cube.data[i, j])
                        self.geom.append(Point(x, y))
                        # i and j represent the index values of the coords, so
                        # they need to stop counting at the end of the coords.
                        if j < len(self.y_coord.points) - 1:
                            j += 1
                    if i < len(self.x_coord.points) - 1:
                        i += 1
                # Now construct pandas dataframe object:
                pandas_df = pd.DataFrame({
                    'x_coord': self.x_coords_pd,
                    'y_coord': self.y_coords_pd,
                    'data': self.data_pd
                })

                # Now make geometry in correct form (which is a list of
                # shapely.geometry.Points objects)
                geo_df = GeoDataFrame(pandas_df, geometry=self.geom)
                dataframes.append(geo_df)

            # Now we have a set of 2D geopandas dataframes which must be
            # stitched back together if required
            if restitch:
                geodataframe = pd.concat(dataframes)
        elif len(self.dims) < 2:
            raise ValueError("Only 2D cubes can be converted to dataframes,"
                             "this cube appears to have only {} dimension."
                             "We can slice up cubes with more than 2 "
                             "dimensions, but we can't give them more "
                             "dimensions if they don't have enough.".format
                             (len(self.dims)))
        else:
            dataframe = as_data_frame(self.cube)
            geodataframe = GeoDataFrame(dataframe, geometry=self.geom)

        if len(self.dims) > 2 and not restitch:
            return dataframes
        else:
            return geodataframe

