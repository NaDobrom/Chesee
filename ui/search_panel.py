"""
Панель поиска
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal


class SearchPanel(QWidget):
    note_selected = pyqtSignal(str)

    def __init__(self, vault_storage, parent=None):
        super().__init__(parent)
        self.vault = vault_storage
        self.setStyleSheet("QWidget { background-color: #1a1b26; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("🔍 ПОИСК")
        header.setStyleSheet(
            "QLabel { background-color: #16161e; color: #7aa2f7; padding: 12px; font-weight: 600; font-size: 11px; letter-spacing: 1px; border-bottom: 1px solid #292e42; }")
        layout.addWidget(header)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите запрос...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #16161e;
                color: #c0caf5;
                border: 1px solid #3b4261;
                border-radius: 6px;
                padding: 10px 14px;
                margin: 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #7aa2f7;
            }
        """)
        self.search_input.textChanged.connect(self.on_search)
        layout.addWidget(self.search_input)

        self.results_list = QListWidget()
        self.results_list.setStyleSheet("""
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
        self.results_list.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.results_list)

    def on_search(self, query: str):
        self.results_list.clear()
        if not query.strip():
            return

        results = self.vault.search(query)
        for note in results:
            item = QListWidgetItem(f"📄 {note.title}")
            item.setData(Qt.ItemDataRole.UserRole, note.title)
            self.results_list.addItem(item)

    def on_item_clicked(self, item):
        title = item.data(Qt.ItemDataRole.UserRole)
        if title:
            self.note_selected.emit(title)