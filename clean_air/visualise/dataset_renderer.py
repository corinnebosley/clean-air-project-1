"""
Top-level module for rendering datasets.
"""

import iris
import xarray
from clean_air.visualise import render_map, render_plot


class DatasetRenderer:
    def __init__(self, dataset):
        # Use iris to read in dataset as lazy array here:
        self.dataset = iris.load_cube(dataset)
        self.dims = self.dataset.dim_coords

        # Guess all possible dim coords here using iris object before loading
        # dataframe as xarray object (but scalar coords become None because we
        # can't make plots out of them):
        for coord in self.dataset.coords():
            axis = iris.util.guess_coord_axis(coord)
            if axis == 'X':
                if len(coord.points) > 1:
                    self.x_coord = coord.name()
                else:
                    self.x_coord = None
            elif axis == 'Y':
                if len(coord.points) > 1:
                    self.y_coord = coord.name()
                else:
                    self.y_coord = None
            elif axis == 'Z':
                if len(coord.points) > 1:
                    self.z_coord = coord.name()
                else:
                    self.z_coord = None
            elif axis == 'T':
                if len(coord.points) > 1:
                    self.t_coord = coord.name()
                else:
                    self.t_coord = None

        # Now load dataset as xarray object as this can read netcdf format
        # and also use the hvplot method:
        self.dataframe = xarray.open_dataset(dataset)

    def render(self):
        """
        Analyses the dimensionality of the dataset and then sends to
        appropriate renderer in render_plot.py or render_map.py.
        """
        # If we have both an x-coord and y-coord then we can draw a map:
        if self.x_coord is not None and self.y_coord is not None:
            self.img_type = 'map'
            render_map.Map(self.dataframe).render(self.x_coord,
                                                  self.y_coord,
                                                  self.z_coord,
                                                  self.t_coord)
        # If we have just a time coord then we can make a timeseries:
        elif self.x_coord is None and self.y_coord is None:
            self.img_type = 'timeseries'
            render_plot.Plot(self.dataframe).render_timeseries()
        # If we don't have any coords then something's gone wrong and we can't
        # plot anything:
        elif (self.x_coord and self.y_coord and self.z_coord and self.t_coord) \
                is None:
            raise ValueError('All dimension coordinates are either missing or '
                             'scalar, please choose a dataset with more '
                             'coordinate points.')



