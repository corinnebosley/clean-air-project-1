"""
Integration tests for module dataframe_converter.py
"""
import os
from clean_air.util import dataframe_converter as dc
import iris
import geopandas


PATH = "/net/home/h06/cbosley/Projects/adaq-aqi/cap-sample-data/model/"


class TestConvertToGeoDF:
    """
    Integration test for class CubeToGeodataframe
    """
    def setup_class(self):
        # This section will have to be modified once first data dump has been
        # merged into cap-sample-data repo.
        self.dataset_path = os.path.join(PATH, "aqum_hourly_so2.nc")
        self.cube = iris.load_cube(self.dataset_path)

    def test_convert_to_geodataframe(self):
        gdf = dc.convert_to_geodf(self.cube, restitch=True)
        assert isinstance(gdf, geopandas.GeoDataFrame)

    def test_convert_to_geodataframe_set(self):
        gdfs = dc.convert_to_geodf(self.cube, restitch=False)
        for gdf in gdfs:
            assert isinstance(gdf, geopandas.GeoDataFrame)
