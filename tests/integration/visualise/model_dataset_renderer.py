"""
Integration tests for the model_dataset_renderer.py visualisations.
"""

import clean_air
import clean_air.visualise.model_dataset_renderer as mdr

MODEL_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/model/"


class TestModelDatasetRenderer:
    """
    Class to test integration properties of model_dataset_renderer.py
    """
    def setup_class(self):
        self.daqi_path = MODEL_DATA_PATH + 'aqum_daily_daqi_mean_20200520.nc'

    def test_renderer_for_daqi(self):
        # Product of renderer will not be an object, it will be an action to
        # produce a plot/graph and send it somewhere to be displayed in the GUI.
        # That means that this call doesn't need an object to return.
        img = mdr.ModelDatasetRenderer(self.daqi_path)
        img.render()


