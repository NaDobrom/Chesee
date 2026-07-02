"""
Проводник файлов
"""

from PyQt6.QtWidgets import (QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout,
                             QLabel, QPushButton, QHBoxLayout, QMenu, QInputDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QAction, QIcon, QPixmap, QPainter
from pathlib import Path


def create_color_icon(hex_color: str, size: int = 12) -> QIcon:
    if not hex_color:
        return QIcon()
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(hex_color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(0, 0, size, size)
    painter.end()
    return QIcon(pixmap)


class FileExplorer(QWidget):
    file_selected = pyqtSignal(str)
    new_note_requested = pyqtSignal()
    rename_requested = pyqtSignal(str, str)
    delete_requested = pyqtSignal(str)

    def __init__(self, vault_path, parent=None):
        super().__init__(parent)
        self.vault_path = Path(vault_path)
        self.current_file = None
        self.setObjectName("file_explorer")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setObjectName("explorer_header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 12, 16, 12)

        title = QLabel("ЗАМЕТКИ")
        title.setObjectName("explorer_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Кнопка создания заметки (ЯРКАЯ и ВИДИМАЯ)
        add_btn = QPushButton("＋")
        add_btn.setToolTip("Новая заметка")
        add_btn.setFixedSize(32, 32)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
                   QPushButton {
                       background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #3b82f6, stop:1 #8b5cf6);
                       color: white;
                       border: none;
                       border-radius: 8px;
                       font-size: 22px;
                       font-weight: bold;
                       padding: 0;
                   }
                   QPushButton:hover {
                       background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #2563eb, stop:1 #7c3aed);
                   }
                   QPushButton:pressed {
                       padding-top: 2px;
                   }
               """)
        add_btn.clicked.connect(lambda: self.new_note_requested.emit())
        header_layout.addWidget(add_btn)

        layout.addWidget(header)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.setObjectName("file_tree")
        self.tree.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.tree)

        self.counter = QLabel()
        self.counter.setObjectName("explorer_counter")
        layout.addWidget(self.counter)

    def refresh(self, storage, current_note=None):
        self.tree.clear()
        self.current_file = current_note

        root_item = QTreeWidgetItem(["📁 Заметки"])
        root_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "root"})
        self.tree.addTopLevelItem(root_item)

        for title in sorted(storage.notes.keys()):
            note = storage.notes[title]
            is_current = (note.title == current_note)

            file_item = QTreeWidgetItem()
            if note.color:
                file_item.setIcon(0, create_color_icon(note.color, 14))

            icon_text = "📌" if is_current else "📄"
            file_item.setText(0, f"{icon_text} {note.title}")
            file_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "note", "title": note.title})
            root_item.addChild(file_item)

        root_item.setExpanded(True)
        self.counter.setText(f"{len(storage.notes)} заметок")

    def on_item_clicked(self, item, column):
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data.get("type") == "note":
            self.file_selected.emit(data["title"])

    def show_context_menu(self, position):
        item = self.tree.itemAt(position)
        if not item:
            return

        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return

        # Запрещаем удалять "Добро пожаловать"
        if data.get("type") == "note" and data.get("title") == "Добро пожаловать":
            return

        menu = QMenu(self)

        if data.get("type") == "note":
            rename_action = QAction("✏️ Переименовать", self)
            rename_action.triggered.connect(lambda: self._do_rename(data["title"]))
            menu.addAction(rename_action)

            delete_action = QAction("️ Удалить", self)
            delete_action.triggered.connect(lambda: self.delete_requested.emit(data["title"]))
            menu.addAction(delete_action)

        menu.exec(self.tree.viewport().mapToGlobal(position))

    def _do_rename(self, title: str):
        new_title, ok = QInputDialog.getText(self, "Переименовать", "Новое название:", text=title)
        if ok and new_title and new_title != title:
            self.rename_requested.emit(title, new_title)