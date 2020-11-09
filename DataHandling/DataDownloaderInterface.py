"""Data Downloader to handle downloading of datasets to storage
   Implement as interface to define API"""

class DataDownloaderInterface:

    def downloadObsDataset(datasetName, fileLocation):
        pass

    def downloadModelGridDataset(datasetName, filelocation):
        pass

    def downloadObsDataset(datasetList): #Func overloading not supported ?
        pass

    def downloadModelGridDataset(datasetList): #Func overloading not supported ?
        pass

 #   def downloadDataset(dataSubset, shapefile):
 #       pass

 #   def downloadDataset(dataSubset, latlong): #Func overloading not supported ?
 #       pass

 #   def downloadDataset(dataSubset, gridbox): #Func overloading not supported ?
 #       pass

 #   def downloadDataset(dataSubset, track): #Func overloading not supported ?
 #       pass