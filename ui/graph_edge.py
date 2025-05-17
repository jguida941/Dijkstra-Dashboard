from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsSimpleTextItem, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QLineF, QPointF
from PyQt6.QtGui import QPen, QColor, QFont, QPainterPath, QBrush, QPolygonF, QFontDatabase
import math

class GraphEdge(QGraphicsPathItem):
    def __init__(self, start_node, end_node, weight):
        super().__init__()
        self.setZValue(0)
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight

        # Set default appearance
        self.setPen(QPen(QColor(100, 100, 100), 2))

        # Add weight label (just the weight value)
        self.label = QGraphicsSimpleTextItem(f"{weight}")
        self.label.setZValue(3)
        # Try to use Orbitron, fall back to system font if not available
        if "Orbitron" in QFontDatabase.families():
            self.label.setFont(QFont("Orbitron", 14, QFont.Weight.ExtraBold))
        else:
            self.label.setFont(QFont("Arial", 14, QFont.Weight.ExtraBold))
        self.label.setBrush(QBrush(QColor("#ffffff")))
        # Add glow effect to the label itself for better pop
        label_glow = QGraphicsDropShadowEffect()
        label_glow.setBlurRadius(15)
        label_glow.setColor(QColor(0, 255, 255, 150))
        label_glow.setOffset(0)
        self.label.setGraphicsEffect(label_glow)

        # Add edge glow effect
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(10)
        self.glow_effect.setOffset(0, 0)
        self.glow_effect.setColor(QColor(0, 255, 255, 100))
        self.setGraphicsEffect(self.glow_effect)

        # Update position when nodes move
        self.start_node.scene().addItem(self)
        self.start_node.scene().addItem(self.label)
        self.update_position()

        self.set_state("default")

    def update_position(self):
        # Calculate control points for curved edge
        start_pos = self.start_node.pos()
        end_pos = self.end_node.pos()

        # Calculate midpoint and control points
        mid = (start_pos + end_pos) / 2
        normal = QPointF(end_pos.y() - start_pos.y(), start_pos.x() - end_pos.x())
        normal_length = (normal.x() ** 2 + normal.y() ** 2) ** 0.5
        if normal_length > 0:
            normal /= normal_length
            # Offset the curve by 20 pixels
            control_point = mid + normal * 20

            # Create curved path
            path = QPainterPath()
            path.moveTo(start_pos)
            path.quadTo(control_point, end_pos)
            self.setPath(path)

            # Add arrow at the end
            arrow_size = 10
            # Use trigonometry for arrowhead
            # Find tangent (direction) at end of path
            line = QLineF(path.pointAtPercent(0.96), path.pointAtPercent(1.0))
            angle_rad = math.radians(-line.angle())

            # Arrowhead points, rotated to align with direction
            arrow_p1 = end_pos + QPointF(
                math.cos(math.radians(line.angle() - 150)) * arrow_size,
                math.sin(math.radians(line.angle() - 150)) * arrow_size
            )
            arrow_p2 = end_pos + QPointF(
                math.cos(math.radians(line.angle() + 150)) * arrow_size,
                math.sin(math.radians(line.angle() + 150)) * arrow_size
            )

            arrow_path = QPainterPath()
            arrow_path.moveTo(end_pos)
            arrow_path.lineTo(arrow_p1)
            arrow_path.lineTo(arrow_p2)
            arrow_path.closeSubpath()

            self.setPath(path + arrow_path)

            # Position weight label at middle of curve, offset for readability
            text_rect = self.label.boundingRect()
            label_pos = path.pointAtPercent(0.5)
            offset = 24
            direction = (self.end_node.pos() - self.start_node.pos())
            length = (direction.x()**2 + direction.y()**2) ** 0.5
            if length != 0:
                direction /= length
            normal = QPointF(-direction.y(), direction.x())  # perpendicular
            label_pos += normal * offset
            self.label.setPos(label_pos.x() - text_rect.width() / 2,
                              label_pos.y() - text_rect.height() / 2)
        else:
            # Fallback to straight line if nodes are too close
            self.setPath(QPainterPath(QLineF(start_pos, end_pos)))
            text_rect = self.label.boundingRect()
            self.label.setPos(mid.x() - text_rect.width()/2,
                            mid.y() - text_rect.height()/2)

    def highlight(self, is_final_path=False):
        if is_final_path:
            self.setPen(QPen(QColor("#00ff00"), 3))  # Bright green
            self.glow_effect.setColor(QColor(0, 255, 0, 150))
            self.glow_effect.setBlurRadius(25)
            self.label.setBrush(QBrush(QColor("#66ff66")))
        else:
            self.setPen(QPen(QColor("#00ffff"), 2))  # Cyan
            self.glow_effect.setColor(QColor(0, 255, 255, 120))
            self.glow_effect.setBlurRadius(15)
            self.label.setBrush(QBrush(QColor("#55ffff")))

    def reset(self):
        self.setPen(QPen(QColor(100, 100, 100), 2))
        self.label.setBrush(QBrush(QColor("#ffffff")))
        self.glow_effect.setColor(QColor(0, 255, 255, 100))
        self.glow_effect.setBlurRadius(10)
    def set_state(self, state):
        label_glow = self.label.graphicsEffect()
        if state == "final":
            self.setPen(QPen(QColor("#00ff00"), 3))  # Bright green
            self.glow_effect.setColor(QColor(0, 255, 0, 180))
            self.glow_effect.setBlurRadius(25)
            self.label.setBrush(QBrush(QColor("#00ff00")))  # Green for used edge
        elif state == "visited":
            self.setPen(QPen(QColor("#00ffff"), 2))  # Cyan
            self.glow_effect.setColor(QColor(0, 255, 255, 120))
            self.glow_effect.setBlurRadius(15)
            self.label.setBrush(QBrush(QColor("#00ffff")))
        elif state == "idle":
            self.setPen(QPen(QColor("#ff0044"), 2))  # Neon red
            self.glow_effect.setColor(QColor(255, 0, 80, 200))
            self.glow_effect.setBlurRadius(30)
            self.label.setBrush(QBrush(QColor("#ff3333")))  # Red for unused edge cost
            if label_glow is not None:
                label_glow.setColor(QColor(255, 0, 80, 200))
        elif state == "default":
            self.setPen(QPen(QColor(100, 100, 100), 2))  # Neutral gray
            self.glow_effect.setColor(QColor(0, 255, 255, 80))
            self.glow_effect.setBlurRadius(8)
            self.label.setBrush(QBrush(QColor("#bbbbbb")))
    def set_cost_label_color(self, color):
        if self.label:
            self.label.setBrush(QBrush(color))
            self.label.update()