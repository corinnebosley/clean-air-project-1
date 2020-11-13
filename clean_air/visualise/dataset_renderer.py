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
        # dataframe as xarray object:
        for coord in self.dataset.dim_coords:
            axis = iris.util.guess_coord_axis(coord)
            if axis == 'X':
                self.x_coord = coord.name()
            elif axis == 'Y':
                self.y_coord = coord.name()
            elif axis == 'Z':
                self.z_coord = coord.name()
            elif axis == 'T':
                self.time_coord = coord.name()

        # Now load dataset as xarray object as this can read netcdf format
        # and also use the hvplot method:
        self.dataframe = xarray.open_dataset(dataset)

        # TODO: In unit tests, check at this point that the data is lazy.(??)

    def render(self):
        # Need to know dimensionality of dataset here so that we know whether
        # to call render_plot or render_map.
        # Start with two dimensions only, then add checks and amendments to
        # accommodate different dimensionalities:
        if len(self.dims) > 1:
            render_map.Map(self.dataframe).render(self.x_coord,
                                                  self.y_coord)
        # else:
        #     render_plot.render(self.dataframe)
