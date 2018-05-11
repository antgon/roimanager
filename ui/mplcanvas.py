from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, dpi=100, colour=None):
        colour = parent.palette().background().color().getRgbF()
        fig = Figure(dpi=dpi)#, facecolor=colour, edgecolor=colour)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        FigureCanvas.__init__(self, fig)
