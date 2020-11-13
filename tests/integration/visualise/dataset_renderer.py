"""
Integration tests for the dataset_renderer.py visualisations.
"""

import clean_air
import clean_air.visualise.dataset_renderer as dr

MODEL_DATA_PATH = "/net/home/h06/cbosley/Projects/toybox/cap_sample_data/model/"


class TestDatasetRenderer:
    """
    Class to test integration properties of dataset_renderer.py
    """
    def setup_class(self):
        self.daqi_path = MODEL_DATA_PATH + 'aqum_daily_daqi_mean_20200520.nc'

    def test_renderer_for_daqi(self):
        # Product of renderer will not be an object, it will be an action to
        # produce a plot/graph and send it somewhere to be displayed in the GUI.
        # That means that this call doesn't need an object to return.
        img = dr.DatasetRenderer(self.daqi_path)
        img.render()


