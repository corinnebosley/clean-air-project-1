import os

import iris

from clean_air.data import DataSubset

SAMPLEDIR = os.path.expanduser("~cbosley/Projects/toybox/cap_sample_data")

def test_point_subset():
    # Create example dataset
    ds = DataSubset(
        None,
        "aqum",
        os.path.join(SAMPLEDIR, "model", "aqum_daily*"),
        latlon=(100, 200),
    )
    cube = ds.as_cube()

    # X and Y coords should now NOT be dim coords
    xcoord = cube.coord(axis="x", dim_coords=False)
    ycoord = cube.coord(axis="y", dim_coords=False)

    # Check we have the point we asked for
    assert iris.util.array_equal(xcoord.points, [200])
    assert iris.util.array_equal(ycoord.points, [100])

def test_box_subset():
    # Create example dataset
    ds = DataSubset(
        None,
        "aqum",
        os.path.join(SAMPLEDIR, "model", "aqum_daily*"),
        box=(-1000, -2000, 3000, 4000),
    )
    cube = ds.as_cube()

    xcoord = cube.coord(axis="x", dim_coords=True)
    ycoord = cube.coord(axis="y", dim_coords=True)

    # Check we have the points we asked for
    assert iris.util.array_equal(xcoord.points, [0, 2000])
    assert iris.util.array_equal(ycoord.points, [-2000, 0, 2000, 4000])
