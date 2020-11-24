"""
Objects representing data subsets
"""

import iris

from .. import util


class DataSubset():
    def __new__(cls, *args, **kw):
        """
        Intercept creation of a DataSubset object, and defer to a more
        specific type if possible.
        """
        if cls is DataSubset:
            if "latlon" in kw:
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
    def __init__(self, *args, latlon, **kw):
        super().__init__(*args, **kw)
        self.latlon = tuple(latlon)

    def as_cube(self):
        if self._cube is not None:
            return self._cube

        cube = super().as_cube()
        try:
            xcoord, ycoord = util.cubes.get_xy_coords(cube)
            y, x = self.latlon
            cube = cube.interpolate([(xcoord.name(), x),
                                     (ycoord.name(), y)],
                                    iris.analysis.Linear())
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
    def __init__(self, *args, box, **kw):
        super().__init__(*args, **kw)
        self.box = tuple(box)

    def as_cube(self):
        if self._cube is not None:
            return self._cube

        cube = super().as_cube()
        xcoord, ycoord = util.cubes.get_xy_coords(cube)
        xmin, ymin, xmax, ymax = self.box
        y = iris.coords.CoordExtent(ycoord, ymin, ymax)

        constraint = iris.Constraint(coord_values={
            ycoord.name(): lambda cell: ymin <= cell.point <= ymax
        })
        if xcoord.units.modulus:
            # ie there is modular arithmetic to worry about.
            # This can be done by extracting with constraints, but it is
            # more convenient to use cube.intersection, which additionally
            # wraps points into the requested range.
            cube = cube.extract(constraint)
            cube = cube.intersection(
                iris.coords.CoordExtent(xcoord, xmin, xmax)
            )
        else:
            constraint &= iris.Constraint(coord_values={
                xcoord.name(): lambda cell: xmin <= cell.point <= xmax
            })
            cube = cube.extract(constraint)

        self._cube = cube
        return self._cube


class TrackSubset(DataSubset):
    """
    A dataset along a (possibly curved) line.
    """
    def __init__(self, *args, track, **kw):
        super().__init__(*args, **kw)
        self.track = track

class ShapeSubset(DataSubset):
    """
    A dataset cut down to an arbitrary polygonal area.
    """
    def __init__(self, *args, shape, **kw):
        super().__init__(*args, **kw)
        self.shape = shape
