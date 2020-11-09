##Data Visuliser Class to handle rendering of maps and plots##


from DataHandling.DataVisuliserInterface import DataVisuliserInterface


class DataVisuliser(DataVisuliserInterface):


    def __init__(self, datasetList [] ) #declare variable to hold a list of datasets
        self.datasetList[] = datasetlist[]  ## Python syntax !!! want to just declare a list within class !

    def renderPlotOfObsDatasets(datasetList):
        # do Something
        pass

    def renderPlotOfModelGriddedDatasets(datasetList):
        # do Something
        pass

    def renderModelGriddedDataset(dataset):
        # do Something
        pass

    def renderObservationalDataset(dataset):
        # do Something
        #Example here for demo only
        obsRender = new ObsDatasetRenderer;
        obsRenderer.renderfunc(dataset);

        pass

    def _renderMapOfDataset(dataSubset, shapefile):
        #doSomething
        pass

    def _renderPlotOfDataset(dataSubset, latlong):
        # doSomething
        pass

    def _renderPlotOfDataset(dataSubset, gridbox): #Func overloading not supported ??
        # doSomething
        pass

    def _renderPlotOfDataset(dataSubset, track): #Func overloading not supported ??
        # doSomething
        pass