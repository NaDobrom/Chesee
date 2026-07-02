"""
Диалог создания ежедневной заметки
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, pyqtSignal


class DailyNoteDialog(QDialog):
    note_created = pyqtSignal(str, str)

    def __init__(self, date_str: str, parent=None):
        super().__init__(parent)
        self.date_str = date_str
        self.setWindowTitle(f"Ежедневная заметка: {date_str}")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("QDialog { background-color: #1a1b26; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel(f"📅 {date_str}")
        title.setStyleSheet("QLabel { color: #7aa2f7; font-size: 18px; font-weight: bold; }")
        layout.addWidget(title)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Что произошло сегодня?")
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #16161e;
                color: #c0caf5;
                border: 1px solid #3b4261;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.editor)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("QPushButton { background-color: #292e42; color: #c0caf5; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; } QPushButton:hover { background-color: #3b4261; }")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("💾 Сохранить")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7aa2f7, stop:1 #bb9af7); color: white; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; font-weight: 600; }")
        save_btn.clicked.connect(self.save_note)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def save_note(self):
        content = self.editor.toPlainText()
        self.note_created.emit(self.date_str, content)
        self.accept()