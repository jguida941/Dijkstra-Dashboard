from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsDropShadowEffect, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, QPointF, QTimer, QRectF, QPoint
from PyQt6.QtGui import QPen, QBrush, QColor, QLinearGradient, QWheelEvent, QMouseEvent
from .graph_node import GraphNode
from .graph_edge import GraphEdge
from core.dijkstra import shortest_path
import math

class GraphView(QGraphicsView):
    def __init__(self, status_panel=None):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Enhanced rendering settings
        self.setRenderHint(self.renderHints().Antialiasing)
        self.setRenderHint(self.renderHints().SmoothPixmapTransform)
        self.setViewportUpdateMode(self.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Set fixed size and scene rect
        self.setFixedSize(900, 700)
        self.scene.setSceneRect(-400, -300, 800, 600)
        
        # Enhanced background with gradient
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0, QColor(10, 10, 10))
        gradient.setColorAt(1, QColor(20, 20, 20))
        self.setBackgroundBrush(QBrush(gradient))
        
        # Enable pan
        self.setDragMode(self.DragMode.ScrollHandDrag)
        
        # Zoom settings
        self.zoom_level = 1.0
        self.zoom_step = 0.2  # 20% zoom step
        
        # Create zoom controls
        self.create_zoom_controls()
        
        # Store nodes and edges
        self.nodes = {}
        self.edges = {}
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_step)
        self.current_path = []
        self.current_step = 0
        self.visited_order = []
        
        # Status panel reference
        self.status_panel = status_panel
        
        # Setup the graph
        self.setup_graph()
        
    def create_zoom_controls(self):
        # Create a container widget for zoom controls
        controls_widget = QWidget()
        controls_layout = QHBoxLayout()
        controls_widget.setLayout(controls_layout)
        
        # Zoom out button
        zoom_out_btn = QPushButton("-")
        zoom_out_btn.setFixedSize(30, 30)
        zoom_out_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        zoom_out_btn.clicked.connect(self.zoom_out)
        
        # Zoom reset button
        zoom_reset_btn = QPushButton("100%")
        zoom_reset_btn.setFixedSize(50, 30)
        zoom_reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        zoom_reset_btn.clicked.connect(self.reset_zoom)
        
        # Zoom in button
        zoom_in_btn = QPushButton("+")
        zoom_in_btn.setFixedSize(30, 30)
        zoom_in_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        zoom_in_btn.clicked.connect(self.zoom_in)
        
        # Add buttons to layout
        controls_layout.addWidget(zoom_out_btn)
        controls_layout.addWidget(zoom_reset_btn)
        controls_layout.addWidget(zoom_in_btn)
        controls_layout.setSpacing(5)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add controls to the view
        controls_widget.setParent(self)
        controls_widget.move(10, 10)  # Position in top-left corner
        
    def zoom_in(self):
        self.zoom_level += self.zoom_step
        self.set_zoom()
        
    def zoom_out(self):
        self.zoom_level = max(0.2, self.zoom_level - self.zoom_step)
        self.set_zoom()
        
    def reset_zoom(self):
        self.zoom_level = 1.0
        self.set_zoom()
        
    def set_zoom(self):
        # Reset transform
        self.resetTransform()
        # Apply new zoom level
        self.scale(self.zoom_level, self.zoom_level)
        
    def mousePressEvent(self, event):
        # Enable panning on left click
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(self.DragMode.ScrollHandDrag)
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        # Disable panning when mouse is released
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(self.DragMode.NoDrag)
        super().mouseReleaseEvent(event)
        
    def setup_graph(self):
        # Dynamically position nodes in a circle based on number of nodes
        node_names = ['A', 'B', 'C', 'D', 'E', 'F']
        radius = 200
        angle_offset = -math.pi / 2  # Start from top center
        node_positions = {}

        for i, name in enumerate(node_names):
            angle = angle_offset + 2 * math.pi * i / len(node_names)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            node_positions[name] = QPointF(x, y)

        # Clear old scene
        self.scene.clear()
        self.nodes.clear()
        self.edges.clear()

        # Add new nodes
        for name, pos in node_positions.items():
            node = GraphNode(name)
            node.setPos(pos)
            self.nodes[name] = node
            self.scene.addItem(node)

        # Add edges
        edges = [
            ('A', 'B', 5), ('A', 'C', 3), ('A', 'E', 11),
            ('B', 'C', 1), ('B', 'F', 2),
            ('C', 'D', 1), ('C', 'E', 5),
            ('D', 'E', 9), ('D', 'F', 3)
        ]

        for start, end, weight in edges:
            edge = GraphEdge(self.nodes[start], self.nodes[end], weight)
            self.edges[(start, end)] = edge
            self.scene.addItem(edge)
            
    def start_visualization(self, start_node, target_node):
        # Reset all nodes and edges to default state
        self.reset()
        self.visited_order = []
        
        # Run Dijkstra's algorithm
        graph = {
            'A': [('B', 5), ('C', 3), ('E', 11)],
            'B': [('A', 5), ('C', 1), ('F', 2)],
            'C': [('A', 3), ('B', 1), ('D', 1), ('E', 5)],
            'D': [('C', 1), ('E', 9), ('F', 3)],
            'E': [('A', 11), ('C', 5), ('D', 9)],
            'F': [('B', 2), ('D', 3)]
        }
        
        distances, paths = shortest_path(graph, start_node, target_node)
        
        # Store path for animation
        if target_node in paths:
            self.current_path = paths[target_node]
            self.current_step = 0

            # Delay status panel update until animation completes
            pass

            # Start animation
            self.animation_timer.start(500)  # 500ms between steps

    def animate_step(self):
        if self.current_step < len(self.current_path):
            current = self.current_path[self.current_step]
            # Highlight as visited (blue) during animation
            self.nodes[current].highlight(is_final_path=False)
            self.visited_order.append(current)

            if self.current_step > 0:
                prev = self.current_path[self.current_step - 1]
                edge = self.edges.get((prev, current)) or self.edges.get((current, prev))
                if edge:
                    edge.highlight(is_final_path=False)

            # Update status panel
            if self.status_panel:
                self.status_panel.show_path(
                    self.current_path,
                    self.get_total_distance(),
                    self.visited_order
                )

            self.current_step += 1
        else:
            # After animation completes, highlight the final path in green
            final_path_edges = set()
            for i in range(len(self.current_path) - 1):
                current = self.current_path[i]
                next_node = self.current_path[i + 1]
                self.nodes[current].highlight(is_final_path=True)
                edge = self.edges.get((current, next_node)) or self.edges.get((next_node, current))
                if edge:
                    edge.highlight(is_final_path=True)
                    edge.set_cost_label_color(QColor("lime"))
                    final_path_edges.add((current, next_node))
                    final_path_edges.add((next_node, current))  # bidirectional

            # Highlight the last node in the final path
            self.nodes[self.current_path[-1]].highlight(is_final_path=True)

            # Set unused edges to red
            for (start, end), edge in self.edges.items():
                if (start, end) not in final_path_edges:
                    edge.set_state("unused")
                    edge.set_cost_label_color(QColor("red"))

            # Set unused nodes to red
            for name, node in self.nodes.items():
                if name not in self.current_path:
                    node.set_state("unused")

            self.animation_timer.stop()

            # Final status update once animation is fully complete
            if self.status_panel:
                self.status_panel.show_path(
                    self.current_path,
                    self.get_total_distance(),
                    self.current_path
                )

    def get_total_distance(self):
        total = 0
        for i in range(len(self.current_path) - 1):
            current = self.current_path[i]
            next_node = self.current_path[i + 1]
            edge = self.edges.get((current, next_node)) or self.edges.get((next_node, current))
            if edge:
                total += edge.weight
        return total

    def reset(self):
        # Stop any ongoing animation
        self.animation_timer.stop()
        self.current_path = []
        self.current_step = 0
        self.visited_order = []

        # Reset all nodes and edges
        for node in self.nodes.values():
            node.reset()
        for edge in self.edges.values():
            edge.reset()

        # Clear status panel
        if self.status_panel:
            self.status_panel.clear()