"""
Top-level module for rendering datasets.
"""

import matplotlib as mpl
import datashader as ds
import pandas as pd

MODEL_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/model/"
OBS_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/obs/"
AIRCRAFT_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/aircraft/"


class ModelDatasetRenderer:
    def __init__(self, dataset):
        self.dataset = dataset

    def render(self):
        # call some nice drawing tools here and plot the details that you
        # want to see in UI
        pass
