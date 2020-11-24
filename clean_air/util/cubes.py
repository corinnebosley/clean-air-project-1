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
