"""
Профессиональный граф связей с визуальными эффектами
"""

from PyQt6.QtWidgets import QWidget, QToolTip, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, \
    QListWidget, QListWidgetItem, QFrame
from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QBrush, QLinearGradient, QPainterPath
from typing import Dict, Optional, List
import math
import json
from pathlib import Path


class GraphNode:
    def __init__(self, title: str, x: float = 0, y: float = 0, color: str = ""):
        self.title = title
        self.x = x
        self.y = y
        self.radius = 28  # Увеличен размер
        self.color = color
        self.connections: List[str] = []
        self.backlinks: List[str] = []
        self.is_hovered = False
        self.is_selected = False
        self.is_dragging = False
    def contains(self, point: QPointF) -> bool:
        """Проверяет попадает ли точка в узел"""
        distance = math.sqrt((point.x() - self.x) ** 2 + (point.y() - self.y) ** 2)
        return distance <= self.radius

class ConnectNotesDialog(QDialog):
    def __init__(self, vault_storage, parent=None):
        super().__init__(parent)
        self.vault = vault_storage
        self.setWindowTitle("Соединить заметки")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("🔗 Соединить заметки")
        title.setStyleSheet("QLabel { color: #f1f5f9; font-size: 20px; font-weight: bold; }")
        layout.addWidget(title)

        hint = QLabel("Выберите две заметки для создания связи:")
        hint.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(hint)

        label1 = QLabel("Из заметки:")
        label1.setStyleSheet("color: #e2e8f0; font-size: 13px; font-weight: 600;")
        layout.addWidget(label1)

        self.combo1 = QComboBox()
        self.combo1.addItems(sorted(vault_storage.notes.keys()))
        self.combo1.setStyleSheet("""
            QComboBox {
                background-color: #1e293b;
                color: #f1f5f9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid #3b82f6;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: #f1f5f9;
                border: 1px solid #334155;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
        """)
        layout.addWidget(self.combo1)

        arrow = QLabel("↓")
        arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow.setStyleSheet("color: #3b82f6; font-size: 28px; font-weight: bold;")
        layout.addWidget(arrow)

        label2 = QLabel("В заметку:")
        label2.setStyleSheet("color: #e2e8f0; font-size: 13px; font-weight: 600;")
        layout.addWidget(label2)

        self.combo2 = QComboBox()
        self.combo2.addItems(sorted(vault_storage.notes.keys()))
        self.combo2.setStyleSheet("""
            QComboBox {
                background-color: #1e293b;
                color: #f1f5f9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid #3b82f6;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: #f1f5f9;
                border: 1px solid #334155;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
        """)
        layout.addWidget(self.combo2)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #334155;
                border: 1px solid #475569;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        connect_btn = QPushButton("🔗 Соединить")
        connect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        connect_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3b82f6, stop:1 #8b5cf6);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:1 #7c3aed);
            }
        """)
        connect_btn.clicked.connect(self.accept)
        btn_layout.addWidget(connect_btn)
        layout.addLayout(btn_layout)

    def get_notes(self):
        return self.combo1.currentText(), self.combo2.currentText()


class GraphWidget(QWidget):
    node_clicked = pyqtSignal(str)

    def __init__(self, vault_storage, parent=None):
        super().__init__(parent)
        self.vault = vault_storage
        self.nodes: Dict[str, GraphNode] = {}
        self.saved_positions: Dict[str, tuple] = {}
        self.selected_node: Optional[str] = None
        self.hovered_node: Optional[str] = None
        self.dragging_node: Optional[str] = None
        self.drag_offset = QPointF(0, 0)

        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.is_panning = False
        self.pan_start = QPointF(0, 0)

        self.positions_file = Path(__file__).parent.parent / "vault" / ".graph_positions.json"
        self.load_positions()

        self.setMinimumSize(300, 300)
        self.setStyleSheet("background-color: #0f172a;")

        # Инфо-панель связей (профессиональный дизайн)
        self.info_panel = QWidget()
        self.info_panel.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        info_layout = QVBoxLayout(self.info_panel)
        info_layout.setContentsMargins(16, 16, 16, 16)
        info_layout.setSpacing(12)

        self.info_label = QLabel("Выберите заметку")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #f1f5f9;
                font-size: 14px;
                font-weight: 600;
                background: transparent;
            }
        """)
        info_layout.addWidget(self.info_label)

        # Разделитель
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #334155; border: none;")
        info_layout.addWidget(sep)

        self.info_list = QListWidget()
        self.info_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                color: #e2e8f0;
                border: none;
                font-size: 12px;
                outline: none;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-radius: 6px;
                margin: 2px 0;
                background: transparent;
            }
            QListWidget::item:hover {
                background-color: #334155;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
                color: white;
            }
        """)
        info_layout.addWidget(self.info_list)
        self.info_panel.hide()

        self.update_graph()

    def load_positions(self):
        try:
            if self.positions_file.exists():
                self.saved_positions = {k: tuple(v) for k, v in
                                        json.loads(self.positions_file.read_text(encoding='utf-8')).items()}
        except:
            pass

    def save_positions(self):
        try:
            self.positions_file.parent.mkdir(exist_ok=True)
            self.positions_file.write_text(json.dumps({t: [n.x, n.y] for t, n in self.nodes.items()}, indent=2),
                                           encoding='utf-8')
        except:
            pass

    def update_graph(self):
        for t, n in self.nodes.items():
            self.saved_positions[t] = (n.x, n.y)
        self.nodes.clear()

        titles = sorted(self.vault.notes.keys())
        # Исключаем "Добро пожаловать" из графа
        titles = [t for t in titles if t != "Добро пожаловать"]

        if not titles:
            self.update()
            return

        n = len(titles)
        w, h = max(self.width(), 400), max(self.height(), 400)
        cx, cy = w / 2, h / 2

        for i, title in enumerate(titles):
            note = self.vault.notes[title]
            if title in self.saved_positions:
                x, y = self.saved_positions[title]
            else:
                angle = 2 * math.pi * i / n if n > 1 else 0
                radius = min(w, h) * 0.35
                x, y = cx + radius * math.cos(angle), cy + radius * math.sin(angle)

            node = GraphNode(title, x, y, note.color)
            node.connections = list(note.links)
            node.backlinks = list(note.backlinks)
            self.nodes[title] = node

        self.save_positions()
        self.update()

    def connect_notes(self, from_title: str, to_title: str):
        if from_title not in self.nodes or to_title not in self.nodes:
            return
        if to_title not in self.nodes[from_title].connections:
            self.nodes[from_title].connections.append(to_title)
        note = self.vault.notes[from_title]
        if to_title not in note.links:
            self.vault.save_note(from_title, note.content + f"\n\n[[{to_title}]]", color=note.color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Фон с градиентом
        bg_gradient = QLinearGradient(0, 0, 0, self.height())
        bg_gradient.setColorAt(0, QColor("#0f172a"))
        bg_gradient.setColorAt(1, QColor("#1e293b"))
        painter.fillRect(self.rect(), QBrush(bg_gradient))

        if not self.nodes:
            painter.setPen(QPen(QColor("#64748b"), 1))
            font = QFont("Segoe UI", 14)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Нет заметок\nСоздайте первую!")
            return

        painter.save()
        painter.translate(self.pan_x, self.pan_y)
        painter.scale(self.zoom, self.zoom)

        # Рисуем связи (линии)
        for title, node in self.nodes.items():
            for link in node.connections:
                if link in self.nodes:
                    target = self.nodes[link]

                    # Создаём градиентную линию
                    line_gradient = QLinearGradient(QPointF(node.x, node.y), QPointF(target.x, target.y))

                    if node.is_selected or target.is_selected:
                        # Активная связь — яркая
                        line_gradient.setColorAt(0, QColor("#3b82f6"))
                        line_gradient.setColorAt(1, QColor("#8b5cf6"))
                        pen = QPen(QBrush(line_gradient), 2.5)
                    else:
                        # Обычная связь — приглушённая
                        line_gradient.setColorAt(0, QColor("#334155"))
                        line_gradient.setColorAt(1, QColor("#475569"))
                        pen = QPen(QBrush(line_gradient), 1.5)

                    painter.setPen(pen)
                    painter.drawLine(QPointF(node.x, node.y), QPointF(target.x, target.y))

        # Рисуем узлы
        for title, node in self.nodes.items():
            # Определяем цвет узла
            if node.color:
                base_color = QColor(node.color)
            else:
                base_color = QColor("#64748b")

            # Создаём радиальный градиент для объёма
            gradient = QRadialGradient(
                QPointF(node.x - node.radius * 0.3, node.y - node.radius * 0.3),
                node.radius * 1.5
            )

            if node.is_selected:
                # Выбранный узел — яркий с свечением
                gradient.setColorAt(0, base_color.lighter(140))
                gradient.setColorAt(0.7, base_color)
                gradient.setColorAt(1, base_color.darker(120))

                # Рисуем свечение
                glow = QRadialGradient(QPointF(node.x, node.y), node.radius * 2)
                glow.setColorAt(0, QColor(base_color.red(), base_color.green(), base_color.blue(), 80))
                glow.setColorAt(1, QColor(base_color.red(), base_color.green(), base_color.blue(), 0))
                painter.setBrush(QBrush(glow))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPointF(node.x, node.y), node.radius * 2, node.radius * 2)

            elif node.is_hovered:
                # Наведение — светлее
                gradient.setColorAt(0, base_color.lighter(130))
                gradient.setColorAt(1, base_color.darker(110))
            else:
                # Обычный узел
                gradient.setColorAt(0, base_color.lighter(120))
                gradient.setColorAt(1, base_color.darker(130))

            # Рисуем узел
            painter.setBrush(QBrush(gradient))

            if node.is_selected:
                painter.setPen(QPen(base_color.lighter(150), 2))
            else:
                painter.setPen(QPen(base_color.lighter(110), 1.5))

            painter.drawEllipse(QPointF(node.x, node.y), node.radius, node.radius)

            # Подпись под узлом
            painter.setPen(QPen(QColor("#e2e8f0")))
            font = QFont("Segoe UI", 11, QFont.Weight.Medium)
            painter.setFont(font)

            # Обрезаем длинный текст
            display_text = title if len(title) <= 16 else title[:15] + "…"
            text_rect = QRectF(node.x - 70, node.y + node.radius + 6, 140, 18)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, display_text)

        painter.restore()

    def screen_to_graph(self, pos: QPointF) -> QPointF:
        return QPointF((pos.x() - self.pan_x) / self.zoom, (pos.y() - self.pan_y) / self.zoom)

    def mousePressEvent(self, event):
        try:
            pos = event.position()
            graph_pos = self.screen_to_graph(pos)
            for title, node in self.nodes.items():
                if node.contains(graph_pos):
                    self.selected_node = title
                    self.dragging_node = title
                    node.is_dragging = True
                    self.drag_offset = QPointF(node.x - graph_pos.x(), node.y - graph_pos.y())
                    for n in self.nodes.values():
                        n.is_selected = False
                    node.is_selected = True
                    self.update()
                    self._show_connections(title)
                    try:
                        self.node_clicked.emit(title)
                    except:
                        pass
                    return
            self.is_panning = True
            self.pan_start = pos
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.selected_node = None
            for n in self.nodes.values():
                n.is_selected = False
            self.info_panel.hide()
            self.update()
        except Exception as e:
            print(f"Ошибка: {e}")

    def mouseMoveEvent(self, event):
        try:
            pos = event.position()
            graph_pos = self.screen_to_graph(pos)
            if self.dragging_node and self.dragging_node in self.nodes:
                node = self.nodes[self.dragging_node]
                node.x = graph_pos.x() + self.drag_offset.x()
                node.y = graph_pos.y() + self.drag_offset.y()
                self.saved_positions[self.dragging_node] = (node.x, node.y)
                self.save_positions()
                self.update()
            elif self.is_panning:
                delta = pos - self.pan_start
                self.pan_x += delta.x()
                self.pan_y += delta.y()
                self.pan_start = pos
                self.update()
            else:
                new_hovered = None
                for title, node in self.nodes.items():
                    if node.contains(graph_pos):
                        new_hovered = title
                        node.is_hovered = True
                        QToolTip.showText(event.globalPosition().toPoint(), title, self)
                        self.setCursor(Qt.CursorShape.PointingHandCursor)
                    else:
                        node.is_hovered = False
                if new_hovered != self.hovered_node:
                    self.hovered_node = new_hovered
                    if not new_hovered:
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                    self.update()
        except:
            pass

    def mouseReleaseEvent(self, event):
        try:
            if self.dragging_node and self.dragging_node in self.nodes:
                self.nodes[self.dragging_node].is_dragging = False
                self.saved_positions[self.dragging_node] = (self.nodes[self.dragging_node].x,
                                                            self.nodes[self.dragging_node].y)
                self.save_positions()
            self.dragging_node = None
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        except:
            pass

    def wheelEvent(self, event):
        try:
            factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
            new_zoom = max(0.3, min(self.zoom * factor, 3.0))
            pos = event.position()
            self.pan_x = pos.x() - (pos.x() - self.pan_x) * (new_zoom / self.zoom)
            self.pan_y = pos.y() - (pos.y() - self.pan_y) * (new_zoom / self.zoom)
            self.zoom = new_zoom
            self.update()
        except:
            pass

    def _show_connections(self, title: str):
        node = self.nodes[title]
        self.info_panel.show()
        self.info_label.setText(f"🔗 Связи: {title}")
        self.info_list.clear()

        for link in node.connections:
            self.info_list.addItem(f"➡️ {link}")
        for link in node.backlinks:
            self.info_list.addItem(f"⬅️ {link}")

        if not node.connections and not node.backlinks:
            empty_item = QListWidgetItem("Нет связей")
            empty_item.setForeground(QColor("#64748b"))
            self.info_list.addItem(empty_item)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()
        # Перемещаем инфо-панель в правый нижний угол
        self.info_panel.setParent(self)
        self.info_panel.move(self.width() - 240, self.height() - 180)
        self.info_panel.setFixedSize(220, 160)
        self.info_panel.raise_()