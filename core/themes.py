"""
Профессиональная система тем оформления Chesee
Разработано с учётом психологии цвета и современных UI/UX стандартов
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Theme:
    name: str
    description: str
    colors: Dict[str, str]


THEMES = {
    # === КИБЕРПАНК ===
    "cyberpunk": Theme(
        name="Самый норм",
        description="Да",
        colors={
            # Фоны (3 уровня глубины)
            "bg_primary": "#0a0e27",
            "bg_secondary": "#151b3d",
            "bg_tertiary": "#1f2855",
            "bg_ribbon": "#070a1f",
            "bg_panel": "#0f1535",
            "bg_editor": "#0a0e27",
            "bg_graph": "#0d1230",
            "bg_header": "#1a2247",
            "bg_input": "#151b3d",
            "bg_button": "#1f2855",
            "bg_button_hover": "#2a3570",
            "bg_selection": "#252d5f",
            "bg_hover": "#1a2247",
            "bg_card": "#151b3d",

            # Текст (3 уровня контраста)
            "text_primary": "#ffffff",
            "text_secondary": "#b4c6e7",
            "text_muted": "#6b7fa8",
            "text_accent": "#00f0ff",
            "text_header": "#ff00ff",
            "text_link": "#00f0ff",
            "text_success": "#00ff88",
            "text_warning": "#ffaa00",
            "text_error": "#ff0066",

            # Акценты (градиенты)
            "accent_primary": "#00f0ff",
            "accent_secondary": "#ff00ff",
            "accent_tertiary": "#ffff00",
            "accent_gradient_start": "#00f0ff",
            "accent_gradient_mid": "#7b2ff7",
            "accent_gradient_end": "#ff00ff",

            # Границы
            "border": "#2a3570",
            "border_light": "#3a4590",
            "border_active": "#00f0ff",
            "border_input": "#2a3570",
            "border_button": "#00f0ff",
            "border_card": "#2a3570",

            # Скроллбар
            "scrollbar": "#2a3570",
            "scrollbar_hover": "#00f0ff",
            "scrollbar_track": "#0a0e27",

            # Статусы
            "success": "#00ff88",
            "warning": "#ffaa00",
            "error": "#ff0066",
            "info": "#00f0ff",

            # Специфичные
            "tag_bg": "#ff00ff22",
            "tag_text": "#ff00ff",
            "link_bg": "#00f0ff11",
            "code_bg": "#151b3d",
            "quote_bg": "#151b3d",
            "quote_border": "#ff00ff",
            "shadow": "rgba(0, 240, 255, 0.3)",
            "glow": "rgba(0, 240, 255, 0.5)",
        }
    ),

    # === ДАРК ФЭНТЕЗИ ===
    "dark_fantasy": Theme(
        name="Хз",
        description="Хз",
        colors={
            "bg_primary": "#1a1510",
            "bg_secondary": "#252018",
            "bg_tertiary": "#302820",
            "bg_ribbon": "#12100d",
            "bg_panel": "#1f1a14",
            "bg_editor": "#1a1510",
            "bg_graph": "#1e1812",
            "bg_header": "#2a2318",
            "bg_input": "#252018",
            "bg_button": "#302820",
            "bg_button_hover": "#3d3228",
            "bg_selection": "#3a3020",
            "bg_hover": "#302820",
            "bg_card": "#252018",

            "text_primary": "#f0e6d3",
            "text_secondary": "#c9b896",
            "text_muted": "#8b7355",
            "text_accent": "#d4af37",
            "text_header": "#d4af37",
            "text_link": "#d4af37",
            "text_success": "#6b8e23",
            "text_warning": "#daa520",
            "text_error": "#8b0000",

            "accent_primary": "#8b0000",
            "accent_secondary": "#d4af37",
            "accent_tertiary": "#4a0080",
            "accent_gradient_start": "#8b0000",
            "accent_gradient_mid": "#a52a2a",
            "accent_gradient_end": "#d4af37",

            "border": "#3a3020",
            "border_light": "#4a4030",
            "border_active": "#d4af37",
            "border_input": "#3a3020",
            "border_button": "#8b0000",
            "border_card": "#3a3020",

            "scrollbar": "#3a3020",
            "scrollbar_hover": "#d4af37",
            "scrollbar_track": "#1a1510",

            "success": "#6b8e23",
            "warning": "#daa520",
            "error": "#8b0000",
            "info": "#4a0080",

            "tag_bg": "#8b000022",
            "tag_text": "#d4af37",
            "link_bg": "#d4af3711",
            "code_bg": "#252018",
            "quote_bg": "#252018",
            "quote_border": "#8b0000",
            "shadow": "rgba(139, 0, 0, 0.3)",
            "glow": "rgba(212, 175, 55, 0.5)",
        }
    ),

    # === ЯПОНИЯ ===
    "japan": Theme(
        name="3",
        description="3",
        colors={
            # Фоны (на основе #FFF3B0 — светлый кремовый)
            "bg_primary": "#FFF3B0",
            "bg_secondary": "#f5e9a0",
            "bg_tertiary": "#ebe090",
            "bg_ribbon": "#f8ec9e",
            "bg_panel": "#f5e9a0",
            "bg_editor": "#FFF3B0",
            "bg_graph": "#faf0a8",
            "bg_header": "#ebe090",
            "bg_input": "#ffffff",
            "bg_button": "#E09F3E",
            "bg_button_hover": "#c98a2e",
            "bg_selection": "#ebe090",
            "bg_hover": "#f5e9a0",
            "bg_card": "#ffffff",

            # Текст (на основе #335C67 — тёмный)
            "text_primary": "#335C67",
            "text_secondary": "#4a7a85",
            "text_muted": "#6a9aa5",
            "text_accent": "#E09F3E",
            "text_header": "#335C67",
            "text_link": "#E09F3E",
            "text_success": "#335C67",
            "text_warning": "#E09F3E",
            "text_error": "#9E2A2B",

            # Акценты
            "accent_primary": "#E09F3E",  # Золотой — главный акцент
            "accent_secondary": "#9E2A2B",  # Бордовый — вторичный
            "accent_tertiary": "#335C67",  # Тёмно-бирюзовый — третий
            "accent_gradient_start": "#E09F3E",
            "accent_gradient_mid": "#d49030",
            "accent_gradient_end": "#9E2A2B",

            # Границы
            "border": "#ebe090",
            "border_light": "#f0e898",
            "border_active": "#E09F3E",
            "border_input": "#ebe090",
            "border_button": "#E09F3E",
            "border_card": "#ebe090",

            # Скроллбар
            "scrollbar": "#ebe090",
            "scrollbar_hover": "#E09F3E",
            "scrollbar_track": "#FFF3B0",

            # Статусы
            "success": "#335C67",
            "warning": "#E09F3E",
            "error": "#9E2A2B",
            "info": "#335C67",

            # Специфичные
            "tag_bg": "#E09F3E22",
            "tag_text": "#E09F3E",
            "link_bg": "#E09F3E11",
            "code_bg": "#f5e9a0",
            "quote_bg": "#f5e9a0",
            "quote_border": "#E09F3E",
            "shadow": "rgba(224, 159, 62, 0.3)",
            "glow": "rgba(224, 159, 62, 0.5)",
        }
    ),

    # === ОГОНЬ ===
    "fire": Theme(
        name="4",
        description="4",
        colors={
            # Фоны (на основе #242021 — тёмный)
            "bg_primary": "#242021",
            "bg_secondary": "#2e2a2b",
            "bg_tertiary": "#383435",
            "bg_ribbon": "#1a1718",
            "bg_panel": "#1f1b1c",
            "bg_editor": "#242021",
            "bg_graph": "#221e1f",
            "bg_header": "#2e2a2b",
            "bg_input": "#2e2a2b",
            "bg_button": "#CCBEB3",
            "bg_button_hover": "#d8cec5",
            "bg_selection": "#383435",
            "bg_hover": "#2e2a2b",
            "bg_card": "#2e2a2b",

            # Текст (на основе #CCBEB3 — светлый)
            "text_primary": "#CCBEB3",
            "text_secondary": "#b5a89d",
            "text_muted": "#a39588",
            "text_accent": "#F896A3",
            "text_header": "#F896A3",
            "text_link": "#F896A3",
            "text_success": "#9C9E4A",
            "text_warning": "#CCBEB3",
            "text_error": "#F896A3",

            # Акценты
            "accent_primary": "#F896A3",  # Розовый — главный акцент
            "accent_secondary": "#9C9E4A",  # Оливковый — вторичный
            "accent_tertiary": "#CCBEB3",  # Бежевый — третий
            "accent_gradient_start": "#F896A3",
            "accent_gradient_mid": "#d4a0a8",
            "accent_gradient_end": "#9C9E4A",

            # Границы
            "border": "#383435",
            "border_light": "#423e3f",
            "border_active": "#F896A3",
            "border_input": "#383435",
            "border_button": "#F896A3",
            "border_card": "#383435",

            # Скроллбар
            "scrollbar": "#383435",
            "scrollbar_hover": "#F896A3",
            "scrollbar_track": "#242021",

            # Статусы
            "success": "#9C9E4A",
            "warning": "#CCBEB3",
            "error": "#F896A3",
            "info": "#9C9E4A",

            # Специфичные
            "tag_bg": "#F896A322",
            "tag_text": "#F896A3",
            "link_bg": "#F896A311",
            "code_bg": "#2e2a2b",
            "quote_bg": "#2e2a2b",
            "quote_border": "#F896A3",
            "shadow": "rgba(248, 150, 163, 0.3)",
            "glow": "rgba(248, 150, 163, 0.5)",
        }
    ),

    # === ОКЕАН ===
    "ocean": Theme(
        name="5",
        description="5",
        colors={
            "bg_primary": "#0a1628",
            "bg_secondary": "#0f1f35",
            "bg_tertiary": "#152845",
            "bg_ribbon": "#071020",
            "bg_panel": "#0d1a2e",
            "bg_editor": "#0a1628",
            "bg_graph": "#0d1a2e",
            "bg_header": "#152d4a",
            "bg_input": "#0f1f35",
            "bg_button": "#1a3555",
            "bg_button_hover": "#204065",
            "bg_selection": "#1a3555",
            "bg_hover": "#152d4a",
            "bg_card": "#0f1f35",

            "text_primary": "#e6f3ff",
            "text_secondary": "#99c2ff",
            "text_muted": "#6699cc",
            "text_accent": "#00d4ff",
            "text_header": "#4da6ff",
            "text_link": "#00d4ff",
            "text_success": "#00cc88",
            "text_warning": "#ffaa00",
            "text_error": "#ff4444",

            "accent_primary": "#0080ff",
            "accent_secondary": "#00d4ff",
            "accent_tertiary": "#4da6ff",
            "accent_gradient_start": "#0080ff",
            "accent_gradient_mid": "#00a0ff",
            "accent_gradient_end": "#00d4ff",

            "border": "#1a3555",
            "border_light": "#204065",
            "border_active": "#00d4ff",
            "border_input": "#1a3555",
            "border_button": "#0080ff",
            "border_card": "#1a3555",

            "scrollbar": "#1a3555",
            "scrollbar_hover": "#00d4ff",
            "scrollbar_track": "#0a1628",

            "success": "#00cc88",
            "warning": "#ffaa00",
            "error": "#ff4444",
            "info": "#4da6ff",

            "tag_bg": "#0080ff22",
            "tag_text": "#00d4ff",
            "link_bg": "#00d4ff11",
            "code_bg": "#0f1f35",
            "quote_bg": "#0f1f35",
            "quote_border": "#0080ff",
            "shadow": "rgba(0, 128, 255, 0.3)",
            "glow": "rgba(0, 212, 255, 0.5)",
        }
    )
}

DEFAULT_THEME = "cyberpunk"


def get_theme(theme_id: str) -> Theme:
    return THEMES.get(theme_id, THEMES[DEFAULT_THEME])


def get_all_themes() -> Dict[str, Theme]:
    return THEMES


def get_stylesheet(theme: Theme) -> str:
    """Генерирует профессиональный stylesheet"""
    c = theme.colors

    return """
    QMainWindow {{
        background-color: {bg_primary};
    }}

    QWidget {{
        background-color: {bg_primary};
        color: {text_primary};
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 13px;
    }}

    QPushButton {{
        background-color: {bg_button};
        color: {text_primary};
        border: 1px solid {border_button};
        border-radius: 8px;
        padding: 10px 18px;
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {bg_button_hover};
        border: 1px solid {border_active};
        color: {text_accent};
    }}

    QPushButton:pressed {{
        background-color: {bg_selection};
    }}

    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
        background-color: {bg_input};
        color: {text_primary};
        border: 1px solid {border_input};
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        selection-background-color: {bg_selection};
        selection-color: {text_primary};
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
        border: 1px solid {border_active};
    }}

    QTextEdit, QPlainTextEdit {{
        padding: 20px 28px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
    }}

    QTreeWidget, QListWidget {{
        background-color: {bg_panel};
        color: {text_primary};
        border: none;
        outline: none;
        font-size: 13px;
    }}

    QTreeWidget::item, QListWidget::item {{
        padding: 8px 12px;
        border-radius: 6px;
        margin: 2px 4px;
        color: {text_primary};
        background-color: transparent;
    }}

    QTreeWidget::item:selected, QListWidget::item:selected {{
        background-color: {bg_selection};
        color: {text_accent};
        font-weight: 600;
    }}

    QTreeWidget::item:hover:!selected, QListWidget::item:hover:!selected {{
        background-color: {bg_hover};
    }}

    QLabel {{
        color: {text_primary};
        background-color: transparent;
    }}

    QScrollBar:vertical {{
        border: none;
        background: {scrollbar_track};
        width: 10px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background: {scrollbar};
        min-height: 30px;
        border-radius: 5px;
        margin: 2px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {scrollbar_hover};
    }}

    QScrollBar:horizontal {{
        border: none;
        background: {scrollbar_track};
        height: 10px;
        margin: 0;
    }}

    QScrollBar::handle:horizontal {{
        background: {scrollbar};
        min-width: 30px;
        border-radius: 5px;
        margin: 2px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {scrollbar_hover};
    }}

    QFrame {{
        background-color: {border};
        border: none;
    }}

    QSplitter::handle {{
        background-color: {border};
    }}

    QToolTip {{
        background-color: {bg_secondary};
        color: {text_primary};
        border: 1px solid {border_active};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
    }}

    QMenu {{
        background-color: {bg_secondary};
        color: {text_primary};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 4px;
    }}

    QMenu::item {{
        padding: 8px 16px;
        border-radius: 6px;
        color: {text_primary};
    }}

    QMenu::item:selected {{
        background-color: {bg_selection};
        color: {text_accent};
    }}

    QProgressBar {{
        background-color: {bg_secondary};
        border: none;
        border-radius: 6px;
        height: 12px;
        text-align: center;
        color: {text_primary};
        font-weight: 600;
    }}

    QProgressBar::chunk {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {accent_gradient_start}, 
            stop:0.5 {accent_gradient_mid},
            stop:1 {accent_gradient_end});
        border-radius: 6px;
    }}

    QTabWidget::pane {{
        border: 1px solid {border};
        border-radius: 8px;
        background-color: {bg_editor};
    }}

    QTabBar::tab {{
        background-color: {bg_secondary};
        color: {text_secondary};
        padding: 10px 20px;
        border: 1px solid {border};
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-weight: 500;
    }}

    QTabBar::tab:selected {{
        background-color: {bg_editor};
        color: {text_accent};
        border-bottom: 2px solid {accent_primary};
    }}

    QTabBar::tab:hover:!selected {{
        background-color: {bg_hover};
        color: {text_primary};
    }}

    QDialog {{
        background-color: {bg_primary};
    }}

    QCalendarWidget {{
        background-color: {bg_primary};
        color: {text_primary};
        border: none;
    }}

    QCalendarWidget QWidget {{
        background-color: {bg_primary};
        color: {text_primary};
    }}

    QCalendarWidget QAbstractItemView {{
        background-color: {bg_secondary};
        color: {text_primary};
        selection-background-color: {bg_selection};
        selection-color: {text_accent};
    }}

    QStatusBar {{
        background-color: {bg_ribbon};
        color: {text_secondary};
        border-top: 1px solid {border};
        font-size: 12px;
    }}

    QWidget#ribbon {{
        background-color: {bg_ribbon};
        border-right: 1px solid {border};
    }}

    QPushButton#logo_btn {{
        background-color: transparent;
        color: {accent_primary};
        border: none;
        border-radius: 14px;
        font-size: 32px;
        font-weight: bold;
    }}

    QPushButton#logo_btn:hover {{
        background-color: {bg_hover};
    }}

    QLabel#logo_label {{
        color: {text_muted};
        font-size: 9px;
        font-weight: 500;
    }}

    QFrame#ribbon_sep, QFrame#ribbon_sep2 {{
        background-color: {border};
        border: none;
    }}

    QPushButton#settings_btn {{
        background-color: transparent;
        color: {text_muted};
        border: none;
        border-radius: 14px;
        font-size: 32px;
    }}

    QPushButton#settings_btn:hover {{
        background-color: {bg_hover};
        color: {text_primary};
    }}

    QPushButton[active="true"] {{
        background-color: {bg_selection};
        color: {accent_primary};
    }}

    QLabel[active="true"] {{
        color: {accent_primary};
        font-weight: 600;
    }}

    QWidget#file_explorer {{
        background-color: {bg_panel};
    }}

    QWidget#explorer_header {{
        background-color: {bg_header};
        border-bottom: 1px solid {border};
    }}

    QLabel#explorer_title {{
        color: {accent_primary};
        font-weight: 600;
        font-size: 11px;
        letter-spacing: 1px;
    }}

    QLabel#explorer_counter {{
        color: {text_muted};
        font-size: 11px;
        padding: 8px 16px;
        background-color: {bg_header};
        border-top: 1px solid {border};
    }}

    QTreeWidget#file_tree {{
        background-color: {bg_panel};
        color: {text_primary};
        border: none;
        outline: none;
    }}

    QWidget#note_editor {{
        background-color: {bg_editor};
    }}

    QWidget#tabs_container {{
        background-color: {bg_header};
        border-bottom: 1px solid {border};
    }}

    QWidget#editor_header {{
        background-color: {bg_editor};
        border-bottom: 1px solid {border};
    }}

    QLabel#editor_title {{
        color: {text_primary};
        font-size: 14px;
        font-weight: 600;
    }}

    QPushButton#color_btn {{
        background-color: {bg_button};
        color: {text_primary};
        border: 1px solid {border};
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
    }}

    QPushButton#color_btn:hover {{
        border: 1px solid {border_active};
    }}

    QPushButton#link_toggle {{
        background-color: {bg_button};
        color: {text_primary};
        border: 1px solid {border};
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
    }}

    QLabel#save_indicator {{
        color: {success};
        font-size: 11px;
        font-weight: 500;
    }}

    QTextEdit#main_editor {{
        background-color: {bg_editor};
        color: {text_primary};
        border: none;
        padding: 24px 32px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        selection-background-color: {bg_selection};
    }}

    QStatusBar#main_statusbar {{
        background-color: {bg_ribbon};
        color: {text_secondary};
        border-top: 1px solid {border};
    }}

    QLabel#status_file {{
        color: {accent_primary};
        font-weight: 500;
    }}

    QLabel#status_md {{
        color: {accent_primary};
        background-color: {bg_selection};
        padding: 2px 8px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: 600;
    }}
    """.format(**c)