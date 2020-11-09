##Data Visuliser to handle rendering of maps and plots##
## Implement as interface to define API as this will be toplevel plug in from GUI

class DataVisuliserInterface:

    def render_obs(self):
        pass

    def render_gridded(self):
        pass
