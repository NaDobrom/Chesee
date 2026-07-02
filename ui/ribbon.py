"""
Профессиональная Ribbon панель с настраиваемыми иконками
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel
from PyQt6.QtCore import Qt, pyqtSignal


class Ribbon(QWidget):
    button_clicked = pyqtSignal(str)

    def __init__(self, parent=None, is_gamedev_window=False):
        super().__init__(parent)
        self.is_gamedev_window = is_gamedev_window
        self.setFixedWidth(72)
        self.setObjectName("ribbon")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 12, 4, 12)
        layout.setSpacing(0)

        # Логотип (только в основном окне)
        if not self.is_gamedev_window:
            logo_btn = QPushButton("✦")
            logo_btn.setFixedSize(56, 56)
            logo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            logo_btn.setToolTip("Открыть GameDev Tracker")
            logo_btn.setObjectName("logo_btn")
            logo_btn.clicked.connect(self._open_gamedev)
            layout.addWidget(logo_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

            logo_label = QLabel("GameDev")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setObjectName("logo_label")
            layout.addWidget(logo_label)

            sep = QFrame()
            sep.setFixedHeight(1)
            sep.setObjectName("ribbon_sep")
            layout.addWidget(sep)
            layout.addSpacing(8)

        # === ИКОНКИ И ЦВЕТА ===
        # Формат: (иконка, id, название, цвет_иконки, цвет_текста)
        buttons = [
            ("💬", "explorer", "Заметки", "#E09F3E", "#9E2A2B"),
            ("🔘", "search", "Поиск", "#9E2A2B", "#E09F3E"),
            ("🗨️", "tags", "Теги", "#335C67", "#FFF3B0"),
            ("🧩", "daily", "Дневник", "#FFF3B0", "#335C67"),
        ]

        if self.is_gamedev_window:
            buttons.append(("🎮", "gamedev", "GameDev", "#9C9E4A", "#CCBEB3"))

        self.button_widgets = {}

        for icon, name, label, icon_color, text_color in buttons:
            btn_container = QWidget()
            btn_container.setFixedHeight(76)
            btn_layout = QVBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 8, 0, 0)
            btn_layout.setSpacing(4)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            # Индикатор активности
            indicator = QFrame()
            indicator.setFixedWidth(3)
            indicator.setFixedHeight(52)
            indicator.setStyleSheet(f"background-color: transparent; border-radius: 2px;")
            indicator.hide()

            # Кнопка с иконкой
            btn = QPushButton(icon)
            btn.setFixedSize(56, 56)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {icon_color};
                    border: none;
                    border-radius: 14px;
                    font-size: 28px;
                }}
                QPushButton:hover {{
                    background-color: #F896A3;
                    color: #F896A3;
                }}
            """)
            btn.clicked.connect(lambda checked, n=name: self._on_button_clicked(n))
            btn_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

            # Подпись под иконкой
            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_widget.setWordWrap(True)
            label_widget.setStyleSheet(f"""
                QLabel {{
                    color: {text_color};
                    font-size: 10px;
                    font-weight: 500;
                    padding: 0;
                    margin: 0;
                }}
            """)
            btn_layout.addWidget(label_widget)

            # Контейнер с индикатором
            main_layout = QHBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(4)
            main_layout.addWidget(indicator)
            main_layout.addWidget(btn_container)

            container = QWidget()
            container.setLayout(main_layout)
            layout.addWidget(container)

            self.button_widgets[name] = (btn, label_widget, indicator, icon_color, text_color)

        layout.addStretch()

        # Разделитель перед настройками
        sep2 = QFrame()
        sep2.setFixedHeight(1)
        sep2.setObjectName("ribbon_sep2")
        layout.addWidget(sep2)
        layout.addSpacing(8)

        # Кнопка настроек
        settings_btn = QPushButton("⚙️")
        settings_btn.setToolTip("Настройки")
        settings_btn.setFixedSize(56, 56)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #CCBEB3;
                border: none;
                border-radius: 14px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #2e2a2b;
                color: #F896A3;
            }
        """)
        settings_btn.clicked.connect(self._open_settings)
        layout.addWidget(settings_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _open_gamedev(self):
        print("🎮 Открываю GameDev...")
        try:
            from ui.gamedev_window import GameDevWindow
            from pathlib import Path

            main_window = self.window()

            if hasattr(main_window, 'gamedev_window') and main_window.gamedev_window is not None:
                main_window.gamedev_window.show()
                main_window.gamedev_window.raise_()
                main_window.gamedev_window.activateWindow()
            else:
                vault_path = Path(__file__).parent.parent / "vault"
                main_window.gamedev_window = GameDevWindow(str(vault_path))
                main_window.gamedev_window.main_window = main_window
                main_window.gamedev_window.show()

            if main_window:
                main_window.hide()
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def _open_settings(self):
        parent = self.window()
        if hasattr(parent, 'open_settings'):
            parent.open_settings()

    def _on_button_clicked(self, name: str):
        self.set_active(name)
        self.button_clicked.emit(name)

    def set_active(self, name: str):
        """Активирует кнопку"""
        for btn_name, (btn, label_widget, indicator, icon_color, text_color) in self.button_widgets.items():
            if btn_name == name:
                # Активная кнопка
                indicator.show()
                indicator.setStyleSheet(f"background-color: {icon_color}; border-radius: 2px;")
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #2e2a2b;
                        color: {icon_color};
                        border: none;
                        border-radius: 14px;
                        font-size: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: #383435;
                        color: {icon_color};
                    }}
                """)
                label_widget.setStyleSheet(f"""
                    QLabel {{
                        color: {icon_color};
                        font-size: 10px;
                        font-weight: 600;
                    }}
                """)
            else:
                # Неактивная кнопка
                indicator.hide()
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {icon_color};
                        border: none;
                        border-radius: 14px;
                        font-size: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: #2e2a2b;
                        color: #F896A3;
                    }}
                """)
                label_widget.setStyleSheet(f"""
                    QLabel {{
                        color: {text_color};
                        font-size: 10px;
                        font-weight: 500;
                    }}
                """)