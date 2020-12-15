#! /usr/bin/env python3

from qtpy import QtWidgets, QtCore, QtGui, PYQT5
import sys
import decimal
import numpy as np

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

class MainWindow(QtWidgets.QMainWindow):

    """ Class to run a graphing calculator."""
    
    def __init__(self, parent=None):

        super().__init__(parent)
        self.setWindowTitle("My calculator")

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        self.layout = QtWidgets.QVBoxLayout()
        widget.setLayout(self.layout)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))

#        self.addToolBar(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()
        self.lines = []

        hlayout = QtWidgets.QHBoxLayout()


        button = QtWidgets.QPushButton("redraw")
        button.clicked.connect(self.redraw)
        self.layout.addWidget(button)

        self.grid = None
        self.text = QtWidgets.QLineEdit()
        self.text.setText("x")

        self.grid = QtWidgets.QGridLayout()
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(1, 20)
        self.grid.setColumnStretch(2, 1)

        btc = QtWidgets.QToolButton()
        self.color = "blue"
        btc.setStyleSheet(f"background: {self.color};")
        btc.update()
        self.grid.addWidget(btc, 0, 0)
        self.grid.addWidget(self.text, 0, 1)
    
        self.bgc = QtWidgets.QButtonGroup()
        self.bgc.addButton(btc)
        self.bgc.buttonClicked.connect(self.set_color)
        self.layout.addLayout(self.grid)


        self.redraw()

    def set_color(self, button):
        """ Set line color"""

        self.color = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.color),
                                                     options=QtWidgets.QColorDialog.DontUseNativeDialog).name()

        
        button.setStyleSheet(f"background: {self.color};")
        
    def redraw(self):
        """Redraw graph."""
        
        x = np.linspace(-1.25, 1.25)

        while self.lines:
            self.lines.pop().remove()

        # Move left y-axis and bottim x-axis to centre, passing through (0,0)
        self.ax.spines['left'].set_position(('data',0.0))
        self.ax.spines['bottom'].set_position(('data',0.0))

        # Eliminate upper and right axes
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')

        # Show ticks in the left and lower axes only
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')

        self.ax.set_position([0.025,0.05,0.95, 0.9])
        self.ax.axis(xmin = x[0], xmax=x[-1])


        glb = {'x':x}
        glb.update(np.__dict__)

        self.lines.append(self.ax.plot(x, eval(self.text.text(), glb),color=self.color)[0])

        fig = self.ax.get_figure()
        fig.canvas.draw()
        fig.canvas.blit()

app = QtWidgets.QApplication(sys.argv)
app.setFont(QtGui.QFont("Lucida Grande", 12))
win = MainWindow()

win.show()

if __name__ == "__main__":
    sys.exit(app.exec_())
