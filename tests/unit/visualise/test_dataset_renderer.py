"""
Unit tests for test_dataset_renderer.py
"""

import clean_air.visualise.dataset_renderer as dr
import os
import pytest
import xarray

MODEL_DATA_PATH = ("/net/home/h06/cbosley/Projects/toybox/cap_sample_data/"
                   "model/")
TIMESERIES_PATH = ("/net/home/h06/cbosley/Projects/toybox/cap_sample_data/"
                   "timeseries/")
SCALAR_PATH = ("/net/home/h06/cbosley/Projects/toybox/cap_sample_data/"
               "scalar/")


class TestDatasetRenderer:
    """
    Class to test object initialisation in DatasetRenderer
    """
    def setup_class(self):
        self.data_path = os.path.join(MODEL_DATA_PATH,
                                      'aqum_daily_daqi_mean_20200520.nc')
        self.initialised = dr.DatasetRenderer(self.data_path)

    def test_lazy_iris_data(self):
        # Check that the iris dataset is loaded as lazy data for performance:
        assert self.initialised.dataset.has_lazy_data

    def test_found_dim_coords(self):
        # Check that all of the iris-guessed coords are the ones that we
        # expect it to discover:
        assert self.initialised.x_coord == 'projection_x_coordinate'
        assert self.initialised.y_coord == 'projection_y_coordinate'
        # height and time are scalar coords so will not be collected:
        assert self.initialised.z_coord is None
        assert self.initialised.t_coord is None

    def test_dataframe_is_xarray(self):
        # Check that the dataframe itself is an xarray object:
        assert isinstance(self.initialised.dataframe, xarray.Dataset)


class TestRenderCall:
    """
    Class to test 'render' method of DatasetRenderer
    """
    def setup_class(self):
        self.model_path = os.path.join(MODEL_DATA_PATH,
                                       'aqum_daily_daqi_mean_20200520.nc')
        self.timeseries_path = os.path.join(TIMESERIES_PATH,
                                            'aqum_hourly_no2_modified.nc')
        self.scalar_path = os.path.join(SCALAR_PATH,
                                        'aqum_no2_modified.nc')

    def test_render_map(self):
        # Check that if the data has an x and a y coordinate, the
        # renderer chooses to create a map rather than a plot.
        dframe = dr.DatasetRenderer(self.model_path)
        dframe.render()
        assert dframe.img_type == 'map'

    def test_render_timeseries(self):
        # Check that if we have scalar x and y coordinates but a full time
        # coord, the renderer will choose to make a timeseries:
        dframe = dr.DatasetRenderer(self.timeseries_path)
        dframe.render()
        assert dframe.img_type == 'timeseries'

    def test_render_error(self):
        # Check that if all our coordinates end up set as None, then an
        # error is raised.
        dframe = dr.DatasetRenderer(self.scalar_path)
        with pytest.raises(ValueError):
            dframe.render()


