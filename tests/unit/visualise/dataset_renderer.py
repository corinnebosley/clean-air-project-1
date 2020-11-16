"""
Unit tests for dataset_renderer.py
"""

import clean_air.visualise.dataset_renderer as dr
import xarray

MODEL_DATA_PATH = "/net/home/h06/cbosley/Projects/toybox/cap_sample_data/model/"


class TestDatasetRenderer:
    """
    Class to test object initialisation in DatasetRenderer
    """
    def setup_class(self):
        self.data_path = MODEL_DATA_PATH + 'aqum_daily_daqi_mean_20200520.nc'
        self.initialised = dr.DatasetRenderer(self.data_path)

    def test_lazy_iris_data(self):
        # Check that the iris dataset is loaded as lazy data for performance:
        assert self.initialised.dataset.has_lazy_data

    def test_found_dim_coords(self):
        # Check that all of the iris-guessed coords are the ones that we
        # expect it to discover:
        assert self.initialised.x_coord == 'projection_x_coordinate'
        assert self.initialised.y_coord == 'projection_y_coordinate'
        assert self.initialised.z_coord == 'height'
        assert self.initialised.t_coord == 'time'

    def test_dataframe_is_xarray(self):
        # Check that the dataframe itself is an xarray object:
        assert isinstance(self.initialised.dataframe, xarray.Dataset)


class TestRenderCall:
    """
    Class to test 'render' method of DatasetRenderer
    """



