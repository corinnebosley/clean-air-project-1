"""
Module to create fabulous visualisations of maps from datasets of more
than 2 dimensions.
"""

import hvplot.xarray  # noqa


class Map:
    """
    Class to process data and create a lovely map from it.
    """
    def __init__(self, dataframe):
        self.df = dataframe.load()

    def render(self, x_coord, y_coord, z_coord=None, time_coord=None):
        # NOTE: Must have a a deployed Bokeh Server app or a deployed Panel
        # app to be able to view these plots.
        # NOTE: At this stage this is only displaying data points, without an
        # actual map behind it yet.

        # TODO: work out what to do when we have x and t coords as well
        self.df.hvplot.points(x=x_coord, y=y_coord, datashade=True)


