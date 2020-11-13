"""
Integration tests for the dataset_renderer.py visualisations.
"""

import clean_air
import clean_air.visualise.dataset_renderer as dr

MODEL_DATA_PATH = "/net/home/h06/cbosley/Projects/toybox/cap_sample_data/model/"
OBS_DATA_PATH = "/net/home/h06/cbosley/Projects/toybox/cap_sample_data/obs/"
AIRCRAFT_DATA_PATH = "/net/home/h06/cbosley/Projects/toybox/cap_sample_data/" \
                     "aircraft/"


class TestDatasetRenderer:
    """
    Class to test integration properties of dataset_renderer.py
    """

    def setup_class(self):
        self.model_path = MODEL_DATA_PATH + 'aqum_daily_daqi_mean_20200520.nc'
        self.obs_path = OBS_DATA_PATH + 'ABD_2015.csv'
        self.aircraft_path = AIRCRAFT_DATA_PATH + \
            'clean_air_MOCCA_data_20200121_M265_v0.nc'

    def test_renderer_for_model_data(self):
        # Product of renderer will not be an object, it will be an action to
        # produce a plot/graph and send it somewhere to be displayed in the GUI.
        # That means that this call doesn't need an object to return.
        img = dr.DatasetRenderer(self.model_path)
        img.render()

    def test_renderer_for_obs_data(self):
        # NOTE: This test highlights the fact that iris cannot read csv files,
        # but we need iris to identify coord axes before passing them to the
        # renderer.  We will therefore need to write a converter as I haven't
        # managed to find one yet.
        # TODO: Write csv to nc converter:
        # https://stackoverflow.com/questions/22933855/convert-csv-to-netcdf
        # This test will fail until the converter is completed.
        img = dr.DatasetRenderer(self.obs_path)
        img.render()

    def test_renderer_for_aircraft_data(self):
        img = dr.DatasetRenderer(self.aircraft_path)
        img.render()

