"""
Objects representing data subsets
"""

import numpy as np
import iris
import shapely.geometry, shapely.ops

from clean_air import util


class DataSubset:
    def __new__(cls, *args, **kw):
        """
        Intercept creation of a DataSubset object, and defer to a more
        specific type if possible.
        """
        if cls is DataSubset:
            if "point" in kw:
                return PointSubset(*args, **kw)
            if "box" in kw:
                return BoxSubset(*args, **kw)
            if "track" in kw:
                return TrackSubset(*args, **kw)
            if "shape" in kw:
                return ShapeSubset(*args, **kw)
        return super().__new__(cls)

    def __init__(
        self,
        id,
        name,
        files,
        category=None,
        parameter=None,
        start_time=None,
        end_time=None,
    ):
        self.id = id
        self.name = name
        self.files = files
        self.category = category
        self.parameter = parameter
        self.start_time = start_time
        self.end_time = end_time

        self._cube = None

    def as_cube(self):
        if self._cube is not None:
            return self._cube

        constraints = None
        if self.parameter:
            constraints = constraints & iris.Constraint(self.parameter)
        if self.start_time:
            constraints = constraints & iris.Constraint(
                time=lambda cell: self.start_time <= cell.point
            )
        if self.end_time:
            constraints = constraints & iris.Constraint(
                time=lambda cell: cell.point < self.end_time
            )

        cube = iris.load_cube(self.files, constraints)

        self._cube = cube
        return self._cube


class PointSubset(DataSubset):
    """
    A dataset with 0 spacial dimensions - a single point.
    """

    def __init__(self, *args, point, crs=None, **kw):
        super().__init__(*args, **kw)
        self.point = tuple(point)

        # TODO: consider whether to continue treating None as "same as data",
        # or whether to insist a CRS is provided
        self.crs = crs

    def as_cube(self):
        if self._cube is not None:
            return self._cube

        cube = super().as_cube()

        # Ensure coordinate systems match
        crs = cube.coord_system().as_cartopy_crs()
        point = shapely.geometry.Point(self.point)
        if self.crs is not None:
            point = util.crs.transform_shape(point, self.crs, crs)

        # Interpolate data to the requested point
        try:
            xcoord, ycoord = util.cubes.get_xy_coords(cube)
            x, y = point.xy
            cube = cube.interpolate(
                [(xcoord.name(), x), (ycoord.name(), y)],
                iris.analysis.Linear()
            )
        except iris.exceptions.CoordinateNotFoundError:
            # This implies that the cube is missing an X or Y coord, which
            # we will assume means that it already represents a single point,
            # stored as attributes instead of coords
            pass

        self._cube = cube
        return self._cube


class BoxSubset(DataSubset):
    """
    A dataset limited to an axis-aligned box.
    """

    def __init__(self, *args, box, crs=None, **kw):
        super().__init__(*args, **kw)
        self.box = tuple(box)

        # TODO: consider whether to continue treating None as "same as data",
        # or whether to insist a CRS is provided
        self.crs = crs

    def as_cube(self):
        if self._cube is not None:
            return self._cube

        cube = super().as_cube()

        # Ensure coordinate systems match
        crs = cube.coord_system().as_cartopy_crs()
        box = shapely.geometry.box(*self.box)
        if self.crs is not None:
            box = util.crs.transform_shape(box, self.crs, crs)

        cube = util.cubes.extract_box(cube, box.bounds)

        self._cube = cube
        return self._cube


class TrackSubset(DataSubset):
    """
    A dataset along a (possibly curved) line.
    """

    def __init__(self, *args, track, crs=None, **kw):
        super().__init__(*args, **kw)
        self.track = track
        self.crs = crs


class ShapeSubset(DataSubset):
    """
    A dataset cut down to an arbitrary polygonal area.
    """

    def __init__(self, *args, shape, crs=None, **kw):
        super().__init__(*args, **kw)
        self.shape = shape

        # TODO: consider whether to continue treating None as "same as data",
        # or whether to insist a CRS is provided
        self.crs = crs

    def as_cube(self):
        if self._cube is not None:
            return self._cube

        cube = super().as_cube()

        # Ensure coordinate systems match
        crs = cube.coord_system().as_cartopy_crs()
        shape = self.shape
        if self.crs is not None:
            shape = util.crs.transform_shape(shape, self.crs, crs)

        # The cells must have bounds for shape intersections to have much
        # meaning, especially for shapes that are small compared to the
        # grid size
        xcoord, ycoord = util.cubes.get_xy_coords(cube)
        if not xcoord.has_bounds():
            xcoord.guess_bounds()
        if not ycoord.has_bounds():
            ycoord.guess_bounds()

        # Extract bounding box
        cube = util.cubes.extract_box(cube, shape.bounds)

        # Mask points outside the actual shape
        # Note we need to do the broadcasting manually: numpy is strangely
        # reluctant to do it, no matter which of the many ways of creating
        # a masked array we try
        weights = util.cubes.get_intersection_weights(cube, shape, True)
        mask = np.broadcast_to(weights == 0, cube.shape)
        data = np.ma.array(cube.data, mask=mask)
        cube = cube.copy(data=data)

        self._cube = cube
        return self._cube
