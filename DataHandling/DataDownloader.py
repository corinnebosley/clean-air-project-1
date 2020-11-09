"""Data Downloader to handle downloading of datasets to storage
These can be full datasets or specified data subsets
For subset requests, these must first be filtered by calling the DataHandler before the download can be completed """

from DataHandling import DataDownloaderInterface

#from multipledispatch import dispatch

class DataDownloader(DataDownloaderInterface):

    def downloadObsDataset(datasetName, fileLocation):
        # do something
        pass

    def downloadModelGridDataset(datasetName, filelocation):
        #do something
        pass


    def downloadObsDataset(datasetList):  #Func overloading not supported ?
        # do something
        pass

    def downloadModelGridDataset(datasetList): #Func overloading not supported ?
        # do something
        pass

    def _downloadDataset( dataSubset, shapefile):
        # do something
        pass

    def _downloadDataset(dataSubset, latlong): #Func overloading not supported ?
        # do something
        pass

    def _downloadDataset(dataSubset, gridbox): #Func overloading not supported ?
        # do something
        pass

    def _downloadDataset(dataSubset, track): #Func overloading not supported ?
        # do something
        pass