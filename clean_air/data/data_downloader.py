"""Data Downloader to handle downloading of datasets to storage
These can be full datasets or specified data subsets
For subset requests, these must first be filtered by calling the DataHandler before the download can be completed """

from .data_downloader_interface import DataDownloaderInterface


class DataDownloader(DataDownloaderInterface):

    def download_obs(self, name, path):
        # do something
        pass

    def download_gridded(self, name, path):
        #do something
        pass
