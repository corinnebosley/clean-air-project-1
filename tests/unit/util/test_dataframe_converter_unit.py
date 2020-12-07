"""
Unit tests for dataframe_converter.py
"""

import os
from clean_air.util import dataframe_converter as dc
from clean_air.util.cubes import get_xy_coords
import iris
import geopandas as geopd
import pandas as pd
import numpy as np

PATH = "/net/home/h06/cbosley/Projects/adaq-aqi/cap-sample-data/"


class TestConvertToGeoDF:
    """
    Unit tests for conversion of cubes to GeoDataFrames.  This class will test
    the structural direction of objects through the function depending on the
    number of dimensions they possess.
    """

    def setup_class(self):
        # This section will have to be modified once first data dump has been
        # merged into cap-sample-data repo.
        self.multidim_path = os.path.join(PATH,
                                          "model/aqum_hourly_so2.nc")
        self.multidim_cube = iris.load_cube(self.multidim_path)

        self.doubledim_path = os.path.join(PATH,
                                           "model/aqum_daily_daqi_mean.nc")
        self.doubledim_cube = iris.load_cube(self.doubledim_path)

        self.onedim_path = os.path.join(PATH,
                                        "timeseries/aircraft_o3_timeseries.nc")
        self.onedim_cube = iris.load_cube(self.onedim_path)

    def test_3d_cube(self):
        gdf = dc.convert_to_geodf(self.multidim_cube, restitch=True)
        assert isinstance(gdf, geopd.GeoDataFrame)

    def test_2d_cube(self):
        gdf = dc.convert_to_geodf(self.doubledim_cube, restitch=False)
        assert isinstance(gdf[0], geopd.GeoDataFrame)

    def test_1d_cube_series(self):
        gs = dc.convert_to_geodf(self.onedim_cube)
        assert isinstance(gs, pd.Series)


class TestMakeGeo:
    """
    Unit tests for helper function to convert cubes to GeoDataFrames.  This
    class will test the breakdown of cubes into x-y sub-cubes and their
    subsequent conversion to GeoDataFrames.
    """
    def setup_class(self):
        self.multidim_path = os.path.join(PATH,
                                          "model/aqum_hourly_so2.nc")
        self.multidim_cube = iris.load_cube(self.multidim_path)

        self.doubledim_path = os.path.join(PATH,
                                           "model/aqum_daily_daqi_mean.nc")
        self.doubledim_cube = iris.load_cube(self.doubledim_path)

    def test_3d_cube_conversion(self):
        x_coord, y_coord = get_xy_coords(self.multidim_cube)
        gdfs = dc._make_geo(self.multidim_cube, x_coord, y_coord)
        for gdf in gdfs:
            assert isinstance(gdf, geopd.GeoDataFrame)

    def test_2d_cube_conversion(self):
        x_coord, y_coord = get_xy_coords(self.doubledim_cube)
        gdf = dc._make_geo(self.doubledim_cube, x_coord, y_coord)
        assert isinstance(gdf[0], geopd.GeoDataFrame)

    def test_data_order_3d(self):
        x_coord, y_coord = get_xy_coords(self.multidim_cube)
        expected_data = [3.60000, 3.5, 3.5, 3.5, 3.60000, 3.60000,
                         3.60000, 3.5, 3.70000, 3.70000, 3.60000, 3.60000]
        gdfs = dc._make_geo(self.multidim_cube, x_coord, y_coord)
        rounded_data = np.round(gdfs[0].data.array, decimals=5)
        assert np.all(rounded_data == expected_data)

