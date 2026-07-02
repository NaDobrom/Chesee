"""
Панель ежедневных заметок
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                              QCalendarWidget, QListWidget, QListWidgetItem,
                              QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QColor
from datetime import datetime


class DailyNotesPanel(QWidget):
    daily_note_requested = pyqtSignal(str)

    def __init__(self, vault_storage, parent=None):
        super().__init__(parent)
        self.vault = vault_storage
        self.setStyleSheet("QWidget { background-color: #1a1b26; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("📅 ЕЖЕДНЕВНЫЕ ЗАМЕТКИ")
        header.setStyleSheet("QLabel { background-color: #16161e; color: #7aa2f7; padding: 12px; font-weight: 600; font-size: 11px; letter-spacing: 1px; border-bottom: 1px solid #292e42; }")
        layout.addWidget(header)

        btn_today = QPushButton(" Создать на сегодня")
        btn_today.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_today.setStyleSheet("""
            QPushButton {
                background-color: #292e42;
                color: #c0caf5;
                border: 1px solid #3b4261;
                padding: 10px;
                margin: 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3b4261;
                color: #7aa2f7;
                border: 1px solid #7aa2f7;
            }
        """)
        btn_today.clicked.connect(self.on_create_today)
        layout.addWidget(btn_today)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget { background-color: #1a1b26; color: #c0caf5; border: none; border-radius: 8px; }
            QCalendarWidget QWidget { background-color: #1a1b26; color: #c0caf5; }
            QCalendarWidget QMenu { background-color: #1a1b26; color: #c0caf5; border: 1px solid #3b4261; }
            QCalendarWidget QSpinBox { background-color: #16161e; color: #c0caf5; border: 1px solid #3b4261; border-radius: 4px; padding: 4px; }
            QCalendarWidget QToolButton { background-color: #16161e; color: #c0caf5; border: none; border-radius: 4px; padding: 6px; font-size: 12px; font-weight: 600; }
            QCalendarWidget QToolButton:hover { background-color: #292e42; color: #7aa2f7; }
            QCalendarWidget QWidget#qt_calendar_navigationbar { background-color: #16161e; border-bottom: 1px solid #292e42; }
            QCalendarWidget QAbstractItemView { background-color: #1a1b26; color: #c0caf5; selection-background-color: #292e42; selection-color: #7aa2f7; border: none; padding: 8px; }
            QCalendarWidget QAbstractItemView::item { border-radius: 4px; padding: 4px; }
            QCalendarWidget QAbstractItemView::item:selected { background-color: #292e42; color: #7aa2f7; }
            QCalendarWidget QAbstractItemView::item:hover { background-color: #24283b; }
            QCalendarWidget QAbstractItemView::item:alternate { color: #f7768e; }
        """)
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.clicked.connect(self.on_date_selected)
        layout.addWidget(self.calendar)

        list_header = QLabel("Существующие заметки:")
        list_header.setStyleSheet("QLabel { color: #565f89; font-size: 10px; font-weight: 600; padding: 8px 12px; background-color: #16161e; border-top: 1px solid #292e42; }")
        layout.addWidget(list_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; } QScrollBar:vertical { border: none; background: #1a1b26; width: 8px; } QScrollBar::handle:vertical { background: #3b4261; min-height: 20px; border-radius: 4px; }")

        self.notes_list = QListWidget()
        self.notes_list.setStyleSheet("""
            QListWidget { background-color: #1a1b26; color: #c0caf5; border: none; font-size: 12px; }
            QListWidget::item { padding: 8px 12px; border-radius: 4px; margin: 2px 4px; }
            QListWidget::item:selected { background-color: #292e42; color: #7aa2f7; }
            QListWidget::item:hover:!selected { background-color: #24283b; }
        """)
        self.notes_list.itemClicked.connect(self.on_note_clicked)
        scroll.setWidget(self.notes_list)
        layout.addWidget(scroll, stretch=1)

        self.refresh_list()

    def on_create_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_note_requested.emit(today)

    def on_date_selected(self, date: QDate):
        date_str = date.toString("yyyy-MM-dd")
        self.daily_note_requested.emit(date_str)

    def on_note_clicked(self, item):
        date_str = item.data(Qt.ItemDataRole.UserRole)
        if date_str:
            self.daily_note_requested.emit(date_str)

    def refresh_list(self):
        self.notes_list.clear()
        import re
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        daily_notes = [t for t in self.vault.notes.keys() if date_pattern.match(t)]
        for date_str in sorted(daily_notes, reverse=True):
            item = QListWidgetItem(f"📅 {date_str}")
            item.setData(Qt.ItemDataRole.UserRole, date_str)
            self.notes_list.addItem(item)
        if not daily_notes:
            empty_item = QListWidgetItem("Нет ежедневных заметок")
            empty_item.setForeground(QColor("#565f89"))
            self.notes_list.addItem(empty_item)