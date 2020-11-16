"""
Unit tests for dataset_renderer.py
"""

import clean_air.visualise.dataset_renderer as dr
from clean_air.visualise import render_map, render_plot
import iris
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
    def setup_class(self):
        self.data_path = MODEL_DATA_PATH + 'aqum_daily_daqi_mean_20200520.nc'
#        self.multiple_dims = dr.DatasetRenderer(self.data_path).render()
        # We need to test that we can make plots (instead of maps) if the
        # number of dimension coordinates is less than 2, so we need to make a
        # dataset with only 1 dim coord so that we can test the renderer's
        # ability to determine the type of plot to produce:
        tmp_cube = iris.load_cube(self.data_path)
        self.y_slice = tmp_cube.extract(iris.Constraint(
            projection_y_coordinate=-184000.00000))
        # TODO: Determine the correct min values for the following coordinates:
        # self.x_slice = tmp_cube.extract(iris.Constraint(
        #     projection_x_coordinate=0))
        # self.t_slice = tmp_cube.extract(iris.Constraint(time=0))

    def test_render_map(self):
        # Check that if the data has more than 1 dimension coordinate, the
        # renderer chooses to create a map rather than a plot.
        dframe = dr.DatasetRenderer(self.data_path)
        dframe.render()
        assert dframe.img_type == 'map'

