"""
Helper functions for Iris Cubes
"""

import iris


def get_xy_coords(cube):
    """
    Finds a Cube's X and Y dimension coords.

    Args:
        cube: Cube to get coords of

    Returns:
        xcoord, ycoord: DimCoords in the X and Y directions
    """
    xcoord = cube.coord(axis="x", dim_coords=True)
    ycoord = cube.coord(axis="y", dim_coords=True)
    return xcoord, ycoord


def extract_box(cube, box):
    """
    Extracts a rectangular area from a cube.

    Args:
        cube: Cube to subset
        box (x0, y0, x1, y1): Box defined in terms of its lower-left (x0, y0)
            and upper-right (x1, y1) corners
    """

    def extent_checker(low, high):
        """
        Create a callback function that checks whether a cell is contained
        in a given range.

        For bounded cells, the cell is included iff its bounded region
        has nonempty intersection with the requested interval. Otherwise
        falls back to simply checking the point.
        """
        def cb(cell):
            if cell.bound:
                a, b = cell.bound
                # Sufficient to check a <= high and low <= b.
                # Note that this *does* cover the potential edge case where
                # a requested range is entirely contained by a cell, as
                # this is just a < low < high < b
                return a <= high and low <= b
            return low <= cell.point <= high
        return cb

    xcoord, ycoord = get_xy_coords(cube)
    xmin, ymin, xmax, ymax = box

    constraint = iris.Constraint(coord_values={
        ycoord.name(): extent_checker(ymin, ymax)
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
            xcoord.name(): extent_checker(xmin, xmax)
        })
        cube = cube.extract(constraint)

    return cube
