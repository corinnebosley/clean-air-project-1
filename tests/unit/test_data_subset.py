import os

import numpy as np
import iris
import shapely

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

class TestPolygonSubset:
    def setup_class(self):
        # Define a test polygon (an extremely simple representation of Exeter)
        shape = shapely.geometry.Polygon([
            (289271.9, 93197.0),
            (289351.3, 95110.1),
            (293405.1, 96855.0),
            (296721.1, 94960.3),
            (297165.1, 86966.9),
            (294181.6, 89357.2),
            (291388.0, 89272.6),
        ])

        # Create example dataset
        self.ds = DataSubset(
            None,
            "aqum",
            os.path.join(SAMPLEDIR, "model", "aqum_hourly_o3_20200520.nc"),
            shape=shape,
        )
        self.cube = self.ds.as_cube()

    def test_subset_mask(self):
        # Define corresponding mask (note: this "looks" upside down compared
        # to how it would be plotted)
        expected_mask = np.array(
            [[1, 1, 1, 1, 0],
             [1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1]]
        )

        # Check we have the right mask (on a 2d slice of this 3d cube)
        subcube = next(self.cube.slices_over("time"))
        assert iris.util.array_equal(subcube.data.mask, expected_mask)

    def test_subset_data(self):
        # Simple data check, which, as the mask is taken into account, should
        # be a pretty reliable test
        assert round(self.cube.data.mean(), 8) == 57.66388811
