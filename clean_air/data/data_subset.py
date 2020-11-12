"""
Objects representing data subsets
"""

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

class PointSubset(DataSubset):
    """
    A dataset with 0 spacial dimensions - a single point.
    """
    def __init__(self, *args, latlon, **kw):
        super().__init__(*args, **kw)
        self.latlon = latlon

class BoxSubset(DataSubset):
    """
    A dataset limited to an axis-aligned box.
    """
    def __init__(self, *args, box, **kw):
        super().__init__(*args, **kw)
        self.box = box

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
