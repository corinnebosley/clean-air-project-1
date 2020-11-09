# Object class to hold datasubsets

class DataSubset :

   def __init__(self
                ,datasetUniqueId
                ,datasetName
                ,fileLocation
                ,metadataUniqueId
                ,subsetParameter #this may need to be a list !
                ,shapeFile
                ,latLong
                ,postcode
                ,gridbox
                ,track
                ,category
                ,startTimeDate
                ,endTimeDate
                ):
       #Assign this stuff
        self.datasetUniqueId = datasetUniqueId
        self.datasetName = datasetName
        self.fileLocation = fileLocation
        self.metadataUniqueId = metadataUniqueId
        self.subsetParameter = subsetParameter
        self.shapeFile = shapeFile  #Can only be one of shapefile,latlong,gridbox,track,postcode. Include functionality to limit this..poss subclasses instead.
        self.latLong = latLong
        self.postcode = postcode
        self.gridbox = gridbox
        self.track = track
        self.category = category
        self.startTimeDate =startTimeDate
        self.endTimeDate = endTimeDate


    def getDataset(self):
        return self


   def setDataset(dataset):
       __init__(self) #or something like this !! Call constructor anyway!


# Ensure get/ set for all individual parameters,goodness knows how works in python !! !