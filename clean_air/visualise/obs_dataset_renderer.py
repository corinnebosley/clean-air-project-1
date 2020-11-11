##This just an example file for demo purposes

##Class to render obs datasets
class ObsDatasetRenderer():
    def __init__(self, dataset):
        self.dataset = dataset

    def render(self):
        #This func will include an if statement to check object type before drawing it. eg: if shapefile then renderShapefile etc

        #EXAMPLE: call some nice drawing tools here and plot the details that you want to see in UI
        self.nice_pic()
        self.line_graph()

    def nice_pic():
        #draw a pretty picture
        pass

    def line_graph():
        #draw a line graph
        pass
