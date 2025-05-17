from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QFontDatabase

class StatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Try to use Orbitron, fall back to system font if not available
        if "Orbitron" in QFontDatabase.families():
            title_font = QFont("Orbitron", 14, QFont.Weight.Bold)
            text_font = QFont("Orbitron", 10)
        else:
            title_font = QFont("Arial", 14, QFont.Weight.Bold)
            text_font = QFont("Arial", 10)
        
        # Title
        title = QLabel("Dijkstra Visualizer – AI Enhanced Mode")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00ffff;")
        layout.addWidget(title)
        
        # Legend
        legend = QLabel("🔵 Visited 🟢 Final Path ⚪️ Unvisited")
        legend.setFont(text_font)
        legend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        legend.setStyleSheet("color: #ffffff;")
        layout.addWidget(legend)
        
        # Status text area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setFont(text_font)
        self.status_text.setMinimumHeight(200)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.status_text)
        
        self.setLayout(layout)
        
    def update_status(self, message, color="#ffffff"):
        cursor = self.status_text.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        self.status_text.setTextCursor(cursor)
        self.status_text.ensureCursorVisible()
        
    def clear(self):
        self.status_text.clear()
        
    def show_path(self, path, distance, visited_order):
        self.status_text.clear()

        # Add summary header
        self.update_status(f"✅ Shortest path from {path[0]} to {path[-1]} found!\n", "#00ff00")

        # Show visited order
        self.update_status("Visited Order:", "#00ffff")
        self.update_status(" → ".join(visited_order), "#ffffff")

        # Show final path
        self.update_status("\nShortest Path:", "#00ffff")
        self.update_status(" → ".join(path), "#ffffff")

        # Show total distance
        self.update_status(f"\nTotal Distance: {distance}", "#00ffff")

        # Show path steps with weights
        self.update_status("\nPath Details:", "#00ffff")
        total = 0
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            weight = self.get_edge_weight(current, next_node)
            total += weight
            self.update_status(f"{current} → {next_node} ({weight})", "#ffffff")
        self.update_status(f"Total: {total}", "#00ffff")
        
    def get_edge_weight(self, start, end):
        # This is a placeholder - you'll need to pass the graph to this class
        # or find another way to access edge weights
        weights = {
            ('A', 'B'): 5, ('A', 'C'): 3, ('A', 'E'): 11,
            ('B', 'C'): 1, ('B', 'F'): 2,
            ('C', 'D'): 1, ('C', 'E'): 5,
            ('D', 'E'): 9, ('D', 'F'): 3
        }
        return weights.get((start, end)) or weights.get((end, start)) or 0 