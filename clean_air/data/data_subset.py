# Object class to hold datasubsets

class DataSubset :
    def __init__(
        self,
        id,
        name,
        path,
        meta_id,
        category,
        start_time,
        end_time,
        subset_parameter,
        shapefile=None,
        latlon=None,
        postcode=None,
        gridbox=None,
        track=None,
    ):
        #Assign this stuff
        self.id = id
        self.name = name
        self.path = path
        self.meta_id = meta_id
        self.category = category
        self.start_time = start_time
        self.end_time = end_time
        self.subset_parameter = subset_parameter
        # Can only have one of shapefile, latlon, gridbox, track, postcode.
        # Include functionality to limit this..poss subclasses instead.
        self.shapefile = shapefile
        self.latlon = latlon
        self.postcode = postcode
        self.gridbox = gridbox
        self.track = track
