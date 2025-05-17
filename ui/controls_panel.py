from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton
from PyQt6.QtCore import Qt

class ControlsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Start node selection
        self.start_combo = QComboBox()
        self.start_combo.addItems(['A', 'B', 'C', 'D', 'E', 'F'])
        self.start_combo.setCurrentText('A')
        layout.addWidget(self.start_combo)
        
        # Target node selection
        self.target_combo = QComboBox()
        self.target_combo.addItems(['A', 'B', 'C', 'D', 'E', 'F'])
        self.target_combo.setCurrentText('F')
        layout.addWidget(self.target_combo)
        
        # Run button
        self.run_button = QPushButton("Run Visualization")
        layout.addWidget(self.run_button)
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        layout.addWidget(self.reset_button)
        
        self.setLayout(layout) 