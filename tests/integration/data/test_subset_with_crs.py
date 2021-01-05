import os

import numpy as np
import iris
import shapely, shapely.geometry
import cartopy.crs as ccrs

from clean_air.data import DataSubset
from clean_air import util

SAMPLEDIR = os.path.expanduser("~cbosley/Projects/toybox/cap_sample_data")


def test_latlon_point():
    # Create example dataset
    ds = DataSubset(
        None,
        "aqum",
        os.path.join(SAMPLEDIR, "model", "aqum_daily*"),
        point=(-0.1, 51.5),
        crs=ccrs.Geodetic(),
    )
    cube = ds.as_cube()

    xcoord, ycoord = util.cubes.get_xy_coords(cube)

    # Check we have the point we asked for
    assert iris.util.array_equal(xcoord.points.round(4), [531866.1304])
    assert iris.util.array_equal(ycoord.points.round(4), [179660.9048])


def test_latlon_box():
    # Create example dataset
    ds = DataSubset(
        None,
        "aqum",
        os.path.join(SAMPLEDIR, "model", "aqum_daily*"),
        box=(-4, 50.4, -2.8, 51.2),
        crs=ccrs.Geodetic(),
    )
    cube = ds.as_cube()

    xcoord, ycoord = util.cubes.get_xy_coords(cube)

    # Check we have the points we asked for (multiples of 2000m within
    # each range)
    # Strictly speaking, the transformed box would have slightly curved edges,
    # and the "corner-most" gridpoints would be:
    # tl: (262000, 146000)
    # tr: (344000, 144000)
    # br: (342000, 56000)
    # bl: (258000, 58000)
    # We therefore expect a slightly larger box, covering the minimum and
    # maximum in both directions
    assert iris.util.array_equal(xcoord.points[[0, -1]], [258000, 344000])
    assert iris.util.array_equal(ycoord.points[[0, -1]], [56000, 146000])


class TestLatlonPolygonSubset:
    # This is literally a copy of the unit test, with converted coordinates
    def setup_class(self):
        # Define a test polygon (an extremely simple representation of Exeter)
        shape = shapely.geometry.Polygon([
            (-3.5690, 50.7273),
            (-3.5685, 50.7445),
            (-3.5115, 50.7609),
            (-3.4640, 50.7445),
            (-3.4555, 50.6727),
            (-3.4984, 50.6936),
            (-3.5379, 50.6924),
        ])

        # Create example dataset
        self.ds = DataSubset(
            None,
            "aqum",
            os.path.join(SAMPLEDIR, "model", "aqum_hourly_o3_20200520.nc"),
            shape=shape,
            crs=ccrs.Geodetic(),
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
