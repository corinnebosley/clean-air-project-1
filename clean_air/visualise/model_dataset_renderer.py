"""
Top-level module for rendering datasets.
"""

import iris
import datashader as ds
import dask
import dask.dataframe as dd
import pandas as pd

MODEL_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/model/"
# OBS_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/obs/"
# AIRCRAFT_DATA_PATH = "~cbosley/Projects/toybox/cap_sample_data/aircraft/"


class ModelDatasetRenderer:
    def __init__(self, dataset):
        # Use iris to read in dataset as lazy array here:
        self.dataset = iris.load_cube(dataset)
        # In unit tests, check at this point that the data is lazy.
        self.metadata = self.dataset.cube_metadata
        self.dims = len(self.metadata.dim_coords())

    def render(self):
        # Need to know dimensionality of dataset here so that we know whether
        # to call render_plot or render_map.
        if self.dims > 2:
            render_map.render(self)
