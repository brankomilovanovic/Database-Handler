import subprocess

# Install networkx if not already installed
try:
    import networkx as nx
except ImportError:
    subprocess.call(['pip', 'install', 'networkx'])

# Install matplotlib.pyplot if not already installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    subprocess.call(['pip', 'install', 'matplotlib'])
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
#from pyArango.connection import Connection
#import networkx as nx
#import matplotlib.pyplot as plt


class ArangoGraphWidget(QWidget):
    def __init__(self, graph_data, parent=None):
        super().__init__(parent)
        self.graph_data = graph_data

        # Create a layout for the widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Visualize the graph
        self.visualize_graph()

    def visualize_graph(self):
        # Create a NetworkX graph from the provided data
        G = nx.Graph()
        for edge in self.graph_data:
            G.add_edge(edge["_key"], edge["stage"])

        # Choose a layout algorithm
        layout = nx.spring_layout(G)

        # Visualize the graph using Matplotlib
        nx.draw(G, pos=layout, with_labels=True)

        # Display the graph in the widget
        plt.show()


class MainWindow(QMainWindow):
    def __init__(self, graph_data):
        super().__init__()

        # Set the window title
        self.setWindowTitle("ArangoDB Graph Visualization")

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create the ArangoGraphWidget and add it to the layout
        graph_widget = ArangoGraphWidget(graph_data)
        layout.addWidget(graph_widget)


if __name__ == "__main__":
    # Assuming you have retrieved the graph data from ArangoDB
    graph_data = [
        {"_key": "product1", "name": "Product 1", "stage": "Development"},
        {"_key": "product3", "name": "Product 2", "stage": "Second"},
        {"_key": "product3", "name": "Product 3", "stage": "Development"},
        {"_key": "product3", "name": "Product 4", "stage": "Development"},
        {"_key": "product6", "name": "Product 5", "stage": "Second"},
        {"_key": "product6", "name": "Product 6", "stage": "Development"},
        {"_key": "product7", "name": "Product 7", "stage": "Second"},
        {"_key": "product7", "name": "Product 8", "stage": "Development"}
    ]

    # Create the application
    app = QApplication([])

    # Create the main window and show it
    main_window = MainWindow(graph_data)
    main_window.show()

    # Start the event loop
    app.exec_()
