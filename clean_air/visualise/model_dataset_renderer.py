"""
Top-level module for rendering datasets.
"""

import matplotlib as mpl
import datashader as ds
import dask
import dask.dataframe as dd
import pandas as pd

MODEL_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/model/"
OBS_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/obs/"
AIRCRAFT_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/aircraft/"


class ModelDatasetRenderer:
    def __init__(self, dataset):
        self.dataset = dataset

    def render(self):
        # Need to know dimensionality of dataset here so that we know whether
        # to call render_plot or render_map.
        pass
