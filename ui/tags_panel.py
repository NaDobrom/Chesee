"""
Панель тегов
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor


class TagsPanel(QWidget):
    tag_selected = pyqtSignal(str)

    def __init__(self, vault_storage, parent=None):
        super().__init__(parent)
        self.vault = vault_storage
        self.setStyleSheet("QWidget { background-color: #1a1b26; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("🏷️ ТЕГИ")
        header.setStyleSheet("QLabel { background-color: #16161e; color: #7aa2f7; padding: 12px; font-weight: 600; font-size: 11px; letter-spacing: 1px; border-bottom: 1px solid #292e42; }")
        layout.addWidget(header)

        self.tags_list = QListWidget()
        self.tags_list.setStyleSheet("""
            QListWidget {
                background-color: #1a1b26;
                color: #c0caf5;
                border: none;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-radius: 4px;
                margin: 2px 4px;
            }
            QListWidget::item:selected {
                background-color: #292e42;
                color: #7aa2f7;
            }
            QListWidget::item:hover:!selected {
                background-color: #24283b;
            }
        """)
        self.tags_list.itemClicked.connect(self.on_tag_clicked)
        layout.addWidget(self.tags_list)

        self.refresh()

    def refresh(self):
        self.tags_list.clear()
        tags = self.vault.get_all_tags()
        for tag_name in tags:
            count = len(self.vault.tags[tag_name].notes)
            item = QListWidgetItem(f"# {tag_name} ({count})")
            item.setData(Qt.ItemDataRole.UserRole, tag_name)
            item.setForeground(QColor("#bb9af7"))
            self.tags_list.addItem(item)

    def on_tag_clicked(self, item):
        tag_name = item.data(Qt.ItemDataRole.UserRole)
        if tag_name:
            self.tag_selected.emit(tag_name)