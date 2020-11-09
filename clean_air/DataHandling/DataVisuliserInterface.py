##Data Visuliser to handle rendering of maps and plots##
## Implement as interface to define API as this will be toplevel plug in from GUI

class DataVisuliserInterface:


    def renderPlotOfObsDatasets(datasetList):
        pass

    def renderPlotOfModelGriddedDatasets(datasetList):
        pass

    def renderModelGriddedDataset(dataset):
        pass

    def renderObservationalDataset(dataset):
        pass





 #   def renderMapOfDataset(dataSubset, shapefile):
 #       pass

 #   def renderPlotOfDataset(dataSubset, latlong):
 #       pass

 #   def renderPlotOfDataset(dataSubset, gridbox):
 #       pass

 #   def renderPlotOfDataset(dataSubset, track):
 #       pass