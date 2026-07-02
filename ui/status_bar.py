"""
Профессиональная строка состояния
"""

from PyQt6.QtWidgets import QStatusBar, QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setObjectName("main_statusbar")
        self.setStyleSheet("""
            QStatusBar {
                background-color: #0f172a;
                color: #94a3b8;
                border-top: 1px solid #1e293b;
                font-size: 12px;
                padding: 0 4px;
            }
            QStatusBar::item {
                border: none;
            }
        """)

        # Левая часть
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(12, 0, 0, 0)
        left_layout.setSpacing(20)

        self.current_file = QLabel("Нет открытой заметки")
        self.current_file.setObjectName("status_file")
        self.current_file.setStyleSheet("""
            QLabel {
                color: #3b82f6;
                font-weight: 500;
                font-size: 12px;
                background: transparent;
            }
        """)
        left_layout.addWidget(self.current_file)

        self.word_count = QLabel("0 слов")
        self.word_count.setObjectName("status_words")
        self.word_count.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 12px;
                background: transparent;
            }
        """)
        left_layout.addWidget(self.word_count)

        self.char_count = QLabel("0 символов")
        self.char_count.setObjectName("status_chars")
        self.char_count.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 12px;
                background: transparent;
            }
        """)
        left_layout.addWidget(self.char_count)
        self.addWidget(left_widget, 1)

        # Правая часть
        right_widget = QWidget()
        right_layout = QHBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 12, 0)
        right_layout.setSpacing(16)

        self.cursor_pos = QLabel("стр 1, кол 1")
        self.cursor_pos.setObjectName("status_cursor")
        self.cursor_pos.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 12px;
                background: transparent;
            }
        """)
        right_layout.addWidget(self.cursor_pos)

        md_indicator = QLabel("Markdown")
        md_indicator.setObjectName("status_md")
        md_indicator.setStyleSheet("""
            QLabel {
                color: #3b82f6;
                background-color: #1e293b;
                padding: 3px 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
                border: 1px solid #334155;
            }
        """)
        right_layout.addWidget(md_indicator)
        self.addPermanentWidget(right_widget)

    def update_counts(self, text: str, filename: str = None):
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        self.word_count.setText(f"{words} слов")
        self.char_count.setText(f"{chars} символов")
        if filename:
            self.current_file.setText(f"📄 {filename}")
        else:
            self.current_file.setText("Нет открытой заметки")

    def update_cursor(self, line: int, column: int):
        self.cursor_pos.setText(f"стр {line}, кол {column}")