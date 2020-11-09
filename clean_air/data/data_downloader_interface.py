"""Data Downloader to handle downloading of datasets to storage
   Implement as interface to define API"""

class DataDownloaderInterface:

    def download_obs(self, name, path):
        pass

    def download_gridded(self, name, path):
        pass
