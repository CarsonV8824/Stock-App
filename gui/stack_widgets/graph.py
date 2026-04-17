import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel, QLineEdit, QMessageBox
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns

import pandas as pd

from data.stockData import getStockData

"""Example:
class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create figure and canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # Create layout and add canvas
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Plot with seaborn
        ax = self.figure.add_subplot(111)
        sns.scatterplot(x='col1', y='col2', data=df, ax=ax)
        self.canvas.draw()"""

class Graph(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        text = QLabel(self.get_html())
        text.setAlignment(Qt.AlignCenter & Qt.AlignTop)

        layout.addWidget(text)

        self.stock_name = QLineEdit()
        self.stock_name.returnPressed.connect(self.get_graph)
        layout.addWidget(self.stock_name)

        self.figure = Figure(figsize=(5,4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        self.data = pd.DataFrame({"x":[5,4,3,2], "y":[6,7,8,9]})
        self.ax = self.figure.add_subplot(111)
        sns.lineplot(data=self.data, x="x", y="y", ax=self.ax)
        self.canvas.draw()
        
        layout.addWidget(self.canvas)

    def get_graph(self):
        new_data:pd.DataFrame | None = getStockData(self.stock_name.text())
        if type(new_data) == None:
            QMessageBox.warning(
                self, 
                "Error",
                "Error Getting Stock data. Check inputs"
            )
            return
        self.ax.clear()
        df = new_data.reset_index()
        sns.lineplot(data=df, x="Date", y="Close", ax=self.ax).set_title(f"Stock of {self.stock_name.text()}")
        self.canvas.draw()

    def get_html(self):
        file_path = os.path.join(os.path.dirname(__file__), "graph.html")
        with open(file_path, "r") as f:
            return ''.join(line for line in f)