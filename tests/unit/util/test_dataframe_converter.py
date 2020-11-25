"""
Unit tests for dataframe_converter.py
"""

import iris
import pandas as ps
import geopandas as geopd
import os

PATH = "/net/home/h06/cbosley/Projects/adaq-aqi/cap-sample-data/model/"


class TestCubeToDataframe:
    """
    Unit tests for class CubeToGeodataframe.
    """
    def setup_class(self):
        # This section will have to be modified once first data dump has been
        # merged into cap-sample-data repo.
        self.dataset_path = os.path.join(PATH, "aqum_hourly_so2.nc")
        self.cube = iris.load_cube(self.dataset_path)

    def test_good_coords(self):
        # Check that xy coordinates have been recognized and grabbed:
        input_coord_names = ['projection_y_coordinate',
                             'projection_x_coordinate']


