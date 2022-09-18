
"""Traffic Analysis Project
Author: Lotfi Hasni
Version: 1.1
Since: July 16, 2020
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GraphPlotter():
    """ This class has one function,
        which is used to create a plot graph
    """

    def create_graph(self, master,x,y,t):
        """ Creates graph of given user data
        """
        # Creates Figure
        fig = Figure(figsize = (5,5), dpi = 100)

        # Adds one subplot
        sub = fig.add_subplot(111)
        sub.plot(x,y, marker = 'o')

        # Sets labels
        sub.set_xlabel("Year(X-axis)")
        if t == "TrafficAccidents":
            fig.suptitle('Traffic Max Incidents 2016-2018')
            sub.set_ylabel("Max Number of Incidents (Y-axis)")
        elif t == "TrafficVolume":
            fig.suptitle('Traffic Max Volume 2016-2018')
            sub.set_ylabel("Max Volume (Y-axis)")

        # Creates canvas for graph
        canvas = FigureCanvasTkAgg(fig, master)
        
        canvas.draw()
        
        # Packs canvas into frame
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)