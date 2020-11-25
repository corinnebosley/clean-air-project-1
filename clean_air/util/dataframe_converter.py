"""
This module contains functions to convert between dataframe types.
"""

from iris.pandas import as_data_frame
import pandas as pd
import geopandas as geopd


class CubeToDataframe:
    """
    Class to convert iris-type cubes to pandas-type dataframes.
    """
    def __init__(self, cube):
        self.cube = cube
        self.coords = cube.coords()
        self.dims = cube.dim_coords


    def convert_to_df(self):
        # Iris function iris.pandas.as_data_frame will only convert a
        # 2D cube into a dataframe, so first make sure all data for conversion
        # is sliced into 2D slices:
        good_coords = ['longitude', 'latitude',
                       'grid_longitude', 'grid_latitude',
                       'projection_y_coordinate', 'projection_x_coordinate']
        if len(self.dims) > 2:
            # If there are more than two coords, we need to look for standard
            # xy dimension coords and use them to slice the cube up:
            xy_coords = []
            pandas_dataframes = []
            for dim in self.dims:
                if dim.name() in good_coords:
                    xy_coords.append(dim)
                else:
                    xy_coords = [self.dims[-1].name(),
                                 self.dims[-2].name()]
            for sub_cube in self.cube.slices(xy_coords):
                pandas_df = as_data_frame(sub_cube)
                pandas_dataframes.append(pandas_df)
            # Now we have a set of 2D pandas dataframes which must be
            # stitched back together
            dataframe = pd.concat(pandas_dataframes)
        elif len(self.dims) != 2:
            dataframe = None
            raise ValueError("Only 2D cubes can be converted to dataframes,"
                             "this cube appears to have {} dimensions".format
                             (len(self.dims)))
        else:
            dataframe = as_data_frame(self.cube)

        return dataframe


class DataframeToGeoDataframe:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def convert_to_geodf(self):

