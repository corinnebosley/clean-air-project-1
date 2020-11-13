"""
Module to create fabulous visualisations of maps from datasets of more
than 2 dimensions.
"""

import hvplot.xarray


# NOTE: dask.dataframes can read csv, fwf, json, hdf, orc, parquet, table
# and sql_table.
class Map:
    """
    Class to process data and create a lovely map from it.
    """
    def __init__(self, dataframe):
        self.df = dataframe.load()

    def render(self, x_coord, y_coord, z_coord=None, time_coord=None):
        self.df.hvplot.points(x=x_coord, y=y_coord, datashade=True)
        print('all ok so far...')

