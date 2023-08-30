# class Connection_Mockup:
#     def __init__(self):
#         self.conn = None
import random


#     def connect(self):
#         self.conn = CON.Connection(arangoURL='http://127.0.0.1:8529', username='root', password='root')
    
#     def close(self):
#         if self.conn:
#             self.conn.close()
    
#     def get_connection(self):
#         if not self.conn:
#             self.connect()
#         return self.conn
    


# mock = Connection_Mockup() #mock object

# conn = mock.get_connection() #getting the connection from the mock obj

# db = conn.databases['no'] #all databases in the arango connection

# DATABASE_NAME = 'no'


# graphs = db[DATABASE_NAME].graphs  #Gets the graphs in the selected database

# print(dir(db['no']))


def load_graph_from_db(database, graph_name, loaded_graph):

    graphs = database.graphs

    graph1 = graphs[graph_name] #specific graph

    edge_collection_names = list(graph1.definitions.keys()) # retrieving all of the edge collections associated with the graph


    vertices = [] # Nodes
    edges = [] # Relations

    collections_names = []
    for edge_name in edge_collection_names:
        edge = graph1.definitions[edge_name] 


        vertex_collections_names = edge.fromCollections # Getting the names of the node collections
        vertex_collections_names.extend(edge.toCollections) #Spajanje to i from kolekcija   

        for name in vertex_collections_names:
            if(name not in collections_names):
                collections_names.append(name)
                vertex_aql = f"FOR vertex IN {name} RETURN vertex"
                vertices_cursor = database.AQLQuery(vertex_aql, rawResults=True)
                for vertex in vertices_cursor:
                # if(vertex not in vertices):
                    vertices.append(vertex)


        edge_aql = f"FOR edge IN {edge_name} RETURN edge"

        edges_cursor = database.AQLQuery(edge_aql, rawResults=True)

        for edge in edges_cursor:
            edges.append(edge)



    graph_json = {
        "vertices": vertices,
        "edges": edges
    }

    graph_json_string = json.dumps(graph_json, indent=4)
    unique_graph_json_string = remove_duplicates(loaded_graph, graph_json_string)

    return unique_graph_json_string, graph_json_string, collections_names ## returning the unique graph as a json string, all graph and collection names


def remove_duplicates(graph1, graph2):
    zajednicki_objekti = []
    novi_lista = []

    if not graph1:
        return graph2

    graph1 = json.loads(graph1)
    graph2 = json.loads(graph2)

    for objekt1 in graph1['vertices']:
        for objekt2 in graph2['vertices']:
            if objekt1['_key'] == objekt2['_key']:
                zajednicki_objekti.append(objekt1)
                break

    for objekt in graph2['vertices']:
        if objekt not in zajednicki_objekti:
            novi_lista.append(objekt)

    unique_graphs = {
        "vertices": novi_lista,
        "edges": [objekt for objekt in graph2['edges'] if objekt not in graph1['edges']]
    }

    return json.dumps(unique_graphs, indent=4)


# ------------------------------- CODE COPIED FROM GraphView2.py (Ivan) For testing purposes


import json
import math
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath, QPolygonF
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem, \
    QApplication, QGraphicsPathItem, QGraphicsPolygonItem, QGraphicsTextItem

rad = 15


class WindowClass(QMainWindow):
    def __init__(self):
        super(WindowClass, self).__init__()
        self.view = ViewClass()
        self.setCentralWidget(self.view)


class ViewClass(QGraphicsView):
    def __init__(self):
        super(ViewClass, self).__init__()

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.s = SceneClass()
        self.setScene(self.s)
        self.setRenderHint(QPainter.Antialiasing)


class SceneClass(QGraphicsScene):
    def __init__(self, id=None):
        super(SceneClass, self).__init__()
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.grid = 30
        self.nodes = []
        self.selected_item = None

    def drawBackground(self, painter, rect):
        if False:
            painter = QPainter()
            rect = QRectF()

        painter.fillRect(rect, QColor(30, 30, 30))
        left = int(rect.left()) - int((rect.left()) % self.grid)
        top = int(rect.top()) - int((rect.top()) % self.grid)
        right = int(rect.right())
        bottom = int(rect.bottom())
        lines = []
        for x in range(left, right, self.grid):
            lines.append(QLineF(x, top, x, bottom))
        for y in range(top, bottom, self.grid):
            lines.append(QLineF(left, y, right, y))
        painter.setPen(QPen(QColor(50, 50, 50)))
        painter.drawLines(lines)

    def createGraphFromJson(self, graph_json):
        graph_data = json.loads(graph_json)

        # Create nodes
        for node_data in graph_data['vertices']:  # Modified 
            id = node_data['_id']
            key = node_data['_key']  # Modified
            x = random.uniform(300, -300)
            y = random.uniform(250, -50)
            node = Node(QPointF(x,y), self, id, key)  # Modify position as needed
            self.addItem(node)
            self.nodes.append(node)

        # Create paths
        for line_data in graph_data['edges']:
            from_node = self.findNodeByKey(line_data['_from'])
            to_node = self.findNodeByKey(line_data['_to'])
            if from_node and to_node:
                path = Path(self, from_node, to_node)
                self.addItem(path)

    def findNodeByKey(self, key):
        for node in self.nodes:
            if node.key == key:
                return node
        return None

    def deleteSelectedItem(self):
        if isinstance(self.selected_item, Node):
            # Delete the selected node
            node = self.selected_item
            self.nodes.remove(node)
            self.removeItem(node)

            # Delete paths connected to the selected node
            connected_paths = node.paths[:]
            for path in connected_paths:
                self.deletePath(path)

        elif isinstance(self.selected_item, Path):
            # Delete the selected path
            path = self.selected_item
            self.deletePath(path)

        self.selected_item = None

    def deletePath(self, path):
        # Remove the path from the scene and from connected nodes
        self.removeItem(path)
        path.start_node.paths.remove(path)
        path.end_node.paths.remove(path)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteSelectedItem()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        if mouseEvent.button() == Qt.LeftButton:
            self.selected_item = None
        if mouseEvent.button() == Qt.MidButton:
            key = "0" #new_node['key']
            name = "x"  # new_node['name']
            node = Node(mouseEvent.scenePos(), self, key, name)
            self.addItem(node)
            self.nodes.append(node)
        super().mousePressEvent(mouseEvent)



class Node(QGraphicsEllipseItem):
    def __init__(self, position, scene, key, name):
        super(Node, self).__init__(-rad, -rad, 2 * rad, 2 * rad)

        self.rad = rad
        self.setPos(position)
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(Qt.green)
        self.paths = []

        self.scene = scene
        self.key = key
        self.name = name

        # Create and attach text label
        self.text = QGraphicsTextItem(name, self)
        self.text.setDefaultTextColor(Qt.white)
        self.text.setPos(-rad, -rad - 20)  # Adjust label position as needed

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for path in self.paths:
                path.updatePath()
        return QGraphicsItem.itemChange(self, change, value)

    def addPath(self, path):
        self.paths.append(path)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        if mouseEvent.button() == Qt.LeftButton:
            self.scene.selected_item = self
        if mouseEvent.button() == Qt.RightButton:
            if self.scene.selected_item:
                if isinstance(self.scene.selected_item, Node):
                    from_node = self.scene.selected_item
                    to_node = self
                    if from_node and to_node:
                        path = Path(self.scene, from_node, to_node)
                        self.scene.addItem(path)
        super().mousePressEvent(mouseEvent)


class Path(QGraphicsPathItem):
    def __init__(self, scene, start_node, end_node):
        super(Path, self).__init__()

        self.setPen(QPen(Qt.red, 1.75))
        self.setZValue(-1)
        self.start_node = start_node
        self.end_node = end_node
        self.scene = scene

        self.start_node.addPath(self)
        self.end_node.addPath(self)
        self.scene.addItem(self)
        self.arrowhead_item = None
        self.updatePath()

    def updatePath(self):
        path = QPainterPath()
        path.moveTo(self.start_node.pos())
        path.lineTo(self.end_node.pos())
        self.setPath(path)

        arrowhead_size = 10  # Adjust arrowhead size as needed
        arrowhead_angle = 50  # Adjust arrowhead angle as needed

        line = QLineF(self.start_node.pos(), self.end_node.pos())
        angle = math.atan2(-line.dy(), -line.dx()) + math.pi

        arrowhead_polygon = QPolygonF()
        arrowhead_polygon.append(line.p2() - QPointF(rad * math.cos(angle), rad * math.sin(angle)))
        arrowhead_polygon.append(line.p2() - QPointF(
            (rad + arrowhead_size) * math.cos(angle - arrowhead_angle),
            (rad + arrowhead_size) * math.sin(angle - arrowhead_angle)
        ))
        arrowhead_polygon.append(line.p2() - QPointF(
            (rad + arrowhead_size) * math.cos(angle + arrowhead_angle),
            (rad + arrowhead_size) * math.sin(angle + arrowhead_angle)
        ))

        if self.arrowhead_item is not None:
            self.scene.removeItem(self.arrowhead_item)

        self.arrowhead_item = QGraphicsPolygonItem(arrowhead_polygon, self)
        self.arrowhead_item.setBrush(Qt.red)
        self.arrowhead_item.setPen(QPen(Qt.NoPen))

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        if mouseEvent.button() == Qt.LeftButton:
            self.scene.selected_item = self
        if mouseEvent.button() == Qt.RightButton:
            self.scene.deleteSelectedItem()
        super().mousePressEvent(mouseEvent)


if __name__ == '__main__':
    app = QApplication([])
    wd = WindowClass()
    wd.show()

    scene = wd.view.s
    # scene.createGraphFromJson(load_graph_from_db(db, 'social')) # Loading and viewing

    app.exec_()


