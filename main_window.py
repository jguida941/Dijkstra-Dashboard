from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from ui.graph_view import GraphView
from ui.controls_panel import ControlsPanel
from ui.status_panel import StatusPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dijkstra Path Visualizer")
        self.setMinimumSize(1000, 700)
        
        # Set dark theme
        self.set_dark_theme()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel (graph and controls)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Create and add controls panel
        self.controls_panel = ControlsPanel()
        left_layout.addWidget(self.controls_panel)

        # Right panel (status)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Create and add status panel
        self.status_panel = StatusPanel()
        right_layout.addWidget(self.status_panel)

        # Create and add graph view
        self.graph_view = GraphView()
        left_layout.addWidget(self.graph_view)
        self.graph_view.status_panel = self.status_panel

        # Add panels to main layout
        main_layout.addWidget(left_panel, stretch=2)
        main_layout.addWidget(right_panel, stretch=1)

        # Connect signals
        self.controls_panel.run_button.clicked.connect(self.start_visualization)
        self.controls_panel.reset_button.clicked.connect(self.reset_visualization)

    def set_dark_theme(self):
        # Set dark palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

        self.setPalette(palette)

    def start_visualization(self):
        start_node = self.controls_panel.start_combo.currentText()
        target_node = self.controls_panel.target_combo.currentText()

        # Clear status panel
        self.status_panel.clear()
        self.status_panel.update_status(f"Starting visualization from {start_node} to {target_node}")

        # Run visualization
        self.graph_view.start_visualization(start_node, target_node)
        # Delay status panel update until animation completes
        pass

    def reset_visualization(self):
        self.graph_view.reset()
        self.status_panel.clear()