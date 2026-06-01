"""
stylesheet.py
Houdini Tools Panel — colour palette and Qt stylesheet.
"""

# ─────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────
PALETTE = {
    "bg_deep":       "#0F1117",
    "bg_panel":      "#161A23",
    "bg_card":       "#1E2330",
    "bg_card_hover": "#252C3E",
    "bg_card_press": "#1A2040",
    "accent":        "#E8762B",       # Houdini orange
    "accent_dim":    "#A8501A",
    "text_primary":  "#F0F2F8",     # Brighter white
    "text_secondary":"#A6AEC9",    # Brighter grey
    "text_muted":    "#5C6280",    # Brighter muted
    "border":        "#2A3048",
    "border_hover":  "#E8762B",
    "success":       "#3DCC8E",
    "header_bg":     "#13161E",
}

# ─────────────────────────────────────────────
#  STYLESHEET
# ─────────────────────────────────────────────
STYLESHEET = f"""
QMainWindow, QWidget#root {{
    background: {PALETTE['bg_deep']};
}}

/* ── Header ── */
QWidget#header {{
    background: {PALETTE['header_bg']};
    border-bottom: 1px solid {PALETTE['border']};
}}
QLabel#title {{
    font-family: "Courier New", monospace;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 3px;
    color: {PALETTE['accent']};
}}
QLabel#subtitle {{
    font-size: 10px;
    color: {PALETTE['text_primary']};
    letter-spacing: 1px;
}}

/* ── Category Combo ── */
QComboBox#category_combo {{
    background: {PALETTE['bg_card']};
    color: {PALETTE['text_primary']};
    border: 1px solid {PALETTE['border']};
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 11px;
    font-family: "Courier New", monospace;
    letter-spacing: 1px;
    min-width: 180px;
}}
QComboBox#category_combo:hover {{
    border-color: {PALETTE['accent']};
}}
QComboBox#category_combo::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox#category_combo::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {PALETTE['accent']};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {PALETTE['bg_panel']};
    color: {PALETTE['text_primary']};
    border: 1px solid {PALETTE['border']};
    selection-background-color: {PALETTE['accent_dim']};
    outline: none;
    font-size: 11px;
}}

/* ── Scroll area ── */
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {PALETTE['bg_panel']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {PALETTE['border']};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {PALETTE['accent']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* ── Status bar ── */
QLabel#statusbar {{
    font-size: 10px;
    color: {PALETTE['text_primary']};
    font-family: "Courier New", monospace;
    padding: 4px 8px;
}}
QLabel#statusbar_ok {{
    font-size: 10px;
    color: {PALETTE['success']};
    font-family: "Courier New", monospace;
    padding: 4px 8px;
}}

/* ── Section label ── */
QLabel#section_label {{
    font-size: 10px;
    font-family: "Courier New", monospace;
    color: {PALETTE['text_secondary']};
    letter-spacing: 2px;
    padding: 8px 0 4px 2px;
}}

/* ── Separator ── */
QFrame#sep {{
    color: {PALETTE['border']};
    max-height: 1px;
}}

/* ── Search bar ── */
QLineEdit#search_bar {{
    background: {PALETTE['bg_card']};
    color: {PALETTE['text_primary']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 0 12px;
    font-size: 11px;
    font-family: "Courier New", monospace;
    selection-background-color: {PALETTE['accent_dim']};
}}
QLineEdit#search_bar:focus {{
    border-color: {PALETTE['accent']};
    background: {PALETTE['bg_card_hover']};
}}
QLineEdit#search_bar::placeholder {{
    color: {PALETTE['text_muted']};
}}
"""

