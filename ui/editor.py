"""
Профессиональный редактор заметок
"""

from PyQt6.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QMenu
from PyQt6.QtCore import Qt, pyqtSignal, QRegularExpression
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor


class LinkHighlighter(QSyntaxHighlighter):
    """Делает [[ссылки]] невидимыми"""

    def __init__(self, parent, hide_links=False):
        super().__init__(parent)
        self.hide_links = hide_links

    def highlightBlock(self, text):
        if not self.hide_links:
            return
        pattern = QRegularExpression(r"\[\[([^\]]+)\]\]")
        it = pattern.globalMatch(text)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("#0f172a"))
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class TabButton(QFrame):
    close_clicked = pyqtSignal(str)
    clicked = pyqtSignal(str)

    def __init__(self, title: str, is_active: bool = False, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_active = is_active
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 10, 0)
        layout.setSpacing(10)

        icon = QLabel("📄")
        icon.setStyleSheet("font-size: 14px; background: transparent;")
        layout.addWidget(icon)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.title_label)

        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(22, 22)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setToolTip("Закрыть вкладку")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                border: none;
                border-radius: 6px;
                font-size: 18px;
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
        """)
        self.close_btn.clicked.connect(lambda: self.close_clicked.emit(title))
        layout.addWidget(self.close_btn)

        self._apply_style()

    def _apply_style(self):
        if self.is_active:
            self.setStyleSheet("""
                QFrame {
                    background-color: #1e293b;
                    border: 1px solid #334155;
                    border-bottom: 2px solid #3b82f6;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                }
                QLabel {
                    color: #f1f5f9;
                    font-size: 12px;
                    font-weight: 600;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #0f172a;
                    border: 1px solid transparent;
                    border-bottom: 1px solid #1e293b;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                }
                QFrame:hover {
                    background-color: #162032;
                }
                QLabel {
                    color: #64748b;
                    font-size: 12px;
                }
            """)

    def set_active(self, active: bool):
        self.is_active = active
        self._apply_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.title)


class NoteEditor(QWidget):
    content_changed = pyqtSignal(str)
    tab_close_requested = pyqtSignal(str)
    tab_selected = pyqtSignal(str)
    note_color_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_title = None
        self.open_tabs = []
        self.hide_links = True
        self.current_color = ""
        self.setObjectName("note_editor")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Панель вкладок
        self.tabs_container = QWidget()
        self.tabs_container.setObjectName("tabs_container")
        self.tabs_layout = QHBoxLayout(self.tabs_container)
        self.tabs_layout.setContentsMargins(10, 6, 10, 0)
        self.tabs_layout.setSpacing(4)
        self.tabs_layout.addStretch()
        layout.addWidget(self.tabs_container)

        # Шапка редактора
        self.header = QWidget()
        self.header.setObjectName("editor_header")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(24, 14, 24, 14)

        self.title_label = QLabel("Добро пожаловать")
        self.title_label.setObjectName("editor_title")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #f1f5f9;
                font-size: 15px;
                font-weight: 600;
                background: transparent;
            }
        """)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        self.color_btn = QPushButton("🎨 Цвет")
        self.color_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.color_btn.setObjectName("color_btn")
        self.color_btn.setToolTip("Выбрать цвет заметки для графа")
        self.color_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3b82f6, stop:1 #8b5cf6);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:1 #7c3aed);
            }
            QPushButton:pressed {
                padding-top: 10px;
            }
        """)
        self.color_btn.clicked.connect(self.show_color_menu)
        header_layout.addWidget(self.color_btn)

        self.link_toggle = QPushButton("🔗 Скрыть")
        self.link_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.link_toggle.setObjectName("link_toggle")
        self.link_toggle.setToolTip("Показать/скрыть [[ссылки]]")
        self.link_toggle.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #94a3b8;
                border: 1px solid #334155;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #334155;
                color: #f1f5f9;
                border: 1px solid #475569;
            }
        """)
        self.link_toggle.clicked.connect(self.toggle_links)
        header_layout.addWidget(self.link_toggle)

        self.save_indicator = QLabel("✓ Сохранено")
        self.save_indicator.setObjectName("save_indicator")
        self.save_indicator.setStyleSheet("""
            QLabel {
                color: #10b981;
                font-size: 11px;
                font-weight: 600;
                background: transparent;
                padding: 4px 10px;
                border-radius: 6px;
            }
        """)
        self.save_indicator.hide()
        header_layout.addWidget(self.save_indicator)
        layout.addWidget(self.header)

        # Редактор
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Начните писать...")
        self.editor.setObjectName("main_editor")
        self.editor.setFont(QFont("Consolas", 14))
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                color: #e2e8f0;
                border: none;
                padding: 28px 36px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.7;
                selection-background-color: #3b82f6;
            }
            QTextEdit:focus {
                border: none;
            }
        """)
        self.editor.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.editor)

        # Подсветка ссылок
        self.highlighter = LinkHighlighter(self.editor.document(), self.hide_links)

    def _on_text_changed(self):
        self.content_changed.emit(self.editor.toPlainText())
        self.save_indicator.show()

    def set_content(self, content: str):
        self.editor.blockSignals(True)
        self.editor.setPlainText(content)
        self.editor.blockSignals(False)

    def get_content(self) -> str:
        return self.editor.toPlainText()

    def set_title(self, title: str):
        self.current_title = title
        self.title_label.setText(f" {title}")
        if title not in self.open_tabs:
            self.open_tabs.append(title)
        self._refresh_tabs()

    def _refresh_tabs(self):
        while self.tabs_layout.count() > 1:
            item = self.tabs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for title in self.open_tabs:
            tab = TabButton(title, is_active=(title == self.current_title))
            tab.clicked.connect(self._on_tab_clicked)
            tab.close_clicked.connect(self._on_tab_closed)
            self.tabs_layout.insertWidget(self.tabs_layout.count() - 1, tab)

    def _on_tab_clicked(self, title: str):
        self.tab_selected.emit(title)

    def _on_tab_closed(self, title: str):
        if title in self.open_tabs:
            self.open_tabs.remove(title)
            self.tab_close_requested.emit(title)
            if title == self.current_title and self.open_tabs:
                self.set_title(self.open_tabs[-1])
                self.tab_selected.emit(self.open_tabs[-1])
            elif not self.open_tabs:
                self.current_title = None
                self.title_label.setText("Добро пожаловать")
            self._refresh_tabs()

    def close_current_tab(self):
        if self.current_title:
            self._on_tab_closed(self.current_title)

    def show_color_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e293b;
                color: #f1f5f9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item {
                padding: 10px 20px;
                border-radius: 6px;
                margin: 2px 0;
            }
            QMenu::item:selected {
                background-color: #334155;
                color: #3b82f6;
            }
        """)
        colors = [
            ("Без цвета", ""),
            ("🔵 Синий", "#3b82f6"),
            ("🟣 Фиолетовый", "#8b5cf6"),
            ("🟢 Зелёный", "#10b981"),
            ("🔴 Красный", "#ef4444"),
            ("🟡 Жёлтый", "#f59e0b"),
            ("⚪ Серый", "#64748b"),
            ("🌸 Розовый", "#ec4899"),
            (" Оранжевый", "#f97316"),
        ]
        for label, hex_color in colors:
            action = menu.addAction(label)
            action.triggered.connect(lambda checked, c=hex_color: self.apply_color(c))
        menu.exec(self.color_btn.mapToGlobal(self.color_btn.rect().bottomLeft()))

    def apply_color(self, color_hex: str):
        self.current_color = color_hex
        self.note_color_changed.emit(color_hex)
        if color_hex:
            self.color_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_hex};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    opacity: 0.9;
                }}
            """)
        else:
            self.color_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #3b82f6, stop:1 #8b5cf6);
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #2563eb, stop:1 #7c3aed);
                }
            """)

    def toggle_links(self):
        self.hide_links = not self.hide_links
        self.link_toggle.setText("🔗 Показать" if self.hide_links else "🔗 Скрыть")
        self.highlighter.hide_links = self.hide_links
        self.highlighter.rehighlight()