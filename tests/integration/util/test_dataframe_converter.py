"""
Integration tests for module dataframe_converter.py
"""

from clean_air.util import dataframe_converter as dc
import iris
import geopandas
import pandas
import os


PATH = "/net/home/h06/cbosley/Projects/adaq-aqi/cap-sample-data/model/"


class TestCubeToDataframe:
    """
    Integration test for class CubeToGeodataframe
    """
    def setup_class(self):
        # This section will have to be modified once first data dump has been
        # merged into cap-sample-data repo.
        self.dataset_path = os.path.join(PATH, "aqum_hourly_so2.nc")
        self.cube = iris.load_cube(self.dataset_path)

    def test_conversion(self):
        geodf = dc.CubeToGeodataframe(self.cube).convert_to_df

        # assert isinstance(geodf, geopandas.GeoDataFrame)
        assert isinstance(geodf, pandas.DataFrame)
