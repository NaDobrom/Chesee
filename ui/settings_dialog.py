"""
Диалог настроек
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QComboBox, QFrame, QWidget, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from core.themes import get_all_themes, get_theme, DEFAULT_THEME


class SettingsDialog(QDialog):
    theme_changed = pyqtSignal(str)

    def __init__(self, current_theme_id: str, parent=None):
        super().__init__(parent)
        self.current_theme_id = current_theme_id
        self.setWindowTitle("⚙️ Настройки")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("⚙️ Настройки")
        title.setStyleSheet("QLabel { font-size: 24px; font-weight: bold; color: #7aa2f7; }")
        layout.addWidget(title)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #292e42;")
        layout.addWidget(sep)

        theme_section = QLabel("🎨 Тема оформления")
        theme_section.setStyleSheet("QLabel { font-size: 16px; font-weight: 600; color: #c0caf5; }")
        layout.addWidget(theme_section)

        theme_hint = QLabel("Выберите тему оформления приложения:")
        theme_hint.setStyleSheet("QLabel { color: #787c99; font-size: 12px; }")
        layout.addWidget(theme_hint)

        self.theme_combo = QComboBox()
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #16161e;
                color: #c0caf5;
                border: 1px solid #3b4261;
                border-radius: 6px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid #7aa2f7;
            }
            QComboBox QAbstractItemView {
                background-color: #16161e;
                color: #c0caf5;
                border: 1px solid #3b4261;
                selection-background-color: #292e42;
                selection-color: #7aa2f7;
            }
        """)

        themes = get_all_themes()
        for theme_id, theme in themes.items():
            self.theme_combo.addItem(f"{theme.name} — {theme.description}", theme_id)
            if theme_id == self.current_theme_id:
                self.theme_combo.setCurrentIndex(self.theme_combo.count() - 1)

        layout.addWidget(self.theme_combo)

        preview_label = QLabel("Предпросмотр:")
        preview_label.setStyleSheet("QLabel { color: #787c99; font-size: 12px; margin-top: 8px; }")
        layout.addWidget(preview_label)

        self.preview_widget = QWidget()
        self.preview_widget.setFixedHeight(120)
        self.preview_widget.setStyleSheet(self.get_current_preview_style())
        layout.addWidget(self.preview_widget)

        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #292e42;
                color: #c0caf5;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3b4261;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        apply_btn = QPushButton("💾 Применить")
        apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7aa2f7, stop:1 #bb9af7);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)
        apply_btn.clicked.connect(self.apply_theme)
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)

    def get_current_preview_style(self) -> str:
        theme_id = self.theme_combo.currentData()
        if not theme_id:
            theme_id = DEFAULT_THEME
        theme = get_theme(theme_id)
        c = theme.colors

        return f"""
            QWidget {{
                background-color: {c['bg_primary']};
                border: 1px solid {c['border']};
                border-radius: 8px;
            }}
            QLabel {{
                color: {c['text_primary']};
                padding: 8px;
            }}
        """

    def on_theme_changed(self):
        self.preview_widget.setStyleSheet(self.get_current_preview_style())

    def apply_theme(self):
        theme_id = self.theme_combo.currentData()
        self.theme_changed.emit(theme_id)
        self.accept()