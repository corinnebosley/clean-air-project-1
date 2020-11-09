##This just an example file for demo purposes

##Class to render obs datasets
class ObsDatasetRenderer(dataset):

def __init__(self, dataset):
    self.dataset = dataset


def renderfunc():
    #This fubc will include an if statement to check object type before drawing it. eg: if shapefile then renderShapefile etc

    #call some nice drawing tools here and plot the details that you want to see in UI
    _aNicePic()
    _alineGraph()

def _aNicePic():
     #draw a pretty picture

def _alineGraph():
    #draw a line graph




# def __init__(self, *args):                       #not poss overload constructor..so use this for getaround...
# ie check if object or list passed in first arg
#     print(len(args), 'were passed')
#     if args:
#         print('first argument is of type', type(args[0]))

#     if type(args[0] == dataset then self.dataset = args[0]
#     else if type(args[0] == list then self.datasetList = args[0]
