"""
Acnologia - Houdini Tools Panel.

Usage:
    import main
    main.launch()
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QComboBox, QFrame, QScrollArea,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor

from . import tools_data
from .stylesheet import PALETTE, STYLESHEET
from .widget import ToolButton
from .admin_panel import AdminPanel

# Shared exec namespace — keeps `hou` and other imports alive between tool calls
_EXEC_GLOBALS: dict = {"__builtins__": __builtins__}

# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class HoudiniToolsPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Acnologia")
        self.setMinimumSize(520, 580)
        self.resize(560, 680)
        self.setStyleSheet(STYLESHEET)
        self._last_category = "All Tools"
        self._last_search = ""
        self._last_cols = 0
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._on_resize_finished)
        self._build_ui()
        self._populate_grid("All Tools")

    # ── Grid layout constants ─────────────────
    _BUTTON_MIN_WIDTH = 120
    _GRID_SPACING = 8
    _GRID_MARGIN = 16

    # ── build skeleton ────────────────────────
    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        root.setStyleSheet(f"background: {PALETTE['bg_deep']};")
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._make_header())
        main_layout.addWidget(self._make_toolbar())

        # scroll area
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet("background: transparent;")

        self.grid_container = QWidget()
        self.grid_container.setStyleSheet(f"background: {PALETTE['bg_deep']};")
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(self._GRID_MARGIN, 8, self._GRID_MARGIN, self._GRID_MARGIN)
        self.grid_layout.setSpacing(self._GRID_SPACING)

        self._scroll.setWidget(self.grid_container)
        main_layout.addWidget(self._scroll, 1)
        main_layout.addWidget(self._make_statusbar())

    # ── dynamic column calculation ────────────
    @property
    def _cols(self):
        """Calculate how many columns fit based on available container width."""
        available_width = self.grid_container.width()
        if available_width < self._BUTTON_MIN_WIDTH:
            return 1
        cols = max(1, (available_width + self._GRID_SPACING) // (self._BUTTON_MIN_WIDTH + self._GRID_SPACING))
        return cols

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Debounce — only reflow after the user stops resizing (150ms idle)
        self._resize_timer.start(150)

    def _on_resize_finished(self):
        """Reflow grid only when column count actually changes."""
        new_cols = self._cols
        if new_cols != self._last_cols:
            self._last_cols = new_cols
            self._populate_grid(self._last_category, self._last_search)

    def _make_header(self):
        from PySide6.QtWidgets import QLineEdit

        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(58)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(16, 0, 16, 0)

        # left: logo dot + title
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {PALETTE['accent']}; font-size: 10px;")
        title = QLabel("ACNOLOGIA")
        title.setObjectName("title")

        hl.addWidget(dot)
        hl.addSpacing(6)
        hl.addWidget(title)
        hl.addSpacing(10)
        hl.addStretch()

        # right: search bar (replaces badge)
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setPlaceholderText("🔍  Search tools…")
        self.search_bar.setFixedWidth(200)
        self.search_bar.setFixedHeight(28)
        self.search_bar.textChanged.connect(self._on_search)
        hl.addWidget(self.search_bar)
        return header

    def _make_toolbar(self):
        bar = QWidget()
        bar.setFixedHeight(52)
        bar.setStyleSheet(
            f"background: {PALETTE['bg_panel']}; "
            f"border-bottom: 1px solid {PALETTE['border']};"
        )
        hl = QHBoxLayout(bar)
        hl.setContentsMargins(16, 0, 16, 0)
        hl.setSpacing(10)

        cat_lbl = QLabel("CATEGORY")
        cat_lbl.setStyleSheet(
            f"font-size: 9px; font-family: 'Courier New', monospace; "
            f"color: {PALETTE['text_muted']}; letter-spacing: 2px;"
        )

        self.combo = QComboBox()
        self.combo.setObjectName("category_combo")
        for cat in tools_data.CATEGORIES.keys():
            self.combo.addItem(cat)

        self.combo.currentTextChanged.connect(lambda cat: self._populate_grid(cat, self.search_bar.text().strip()))

        hl.addWidget(cat_lbl)
        hl.addWidget(self.combo)
        hl.addStretch()

        # run-script button (execute last clicked tool again)
        self.run_btn = QPushButton("▶  RE-RUN")
        self.run_btn.setFixedHeight(30)
        self.run_btn.setEnabled(False)
        self.run_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.run_btn.setStyleSheet(
            f"QPushButton {{"
            f"  background: {PALETTE['bg_card']}; color: {PALETTE['text_secondary']}; "
            f"  border: 1px solid {PALETTE['border']}; border-radius: 4px; "
            "  font-size: 10px; font-family: 'Courier New', monospace; "
            "  letter-spacing: 1px; padding: 0 14px;"
            f"}}"
            f"QPushButton:enabled {{"
            f"  background: {PALETTE['accent_dim']}; color: {PALETTE['text_primary']}; "
            f"  border-color: {PALETTE['accent']};"
            f"}}"
            f"QPushButton:enabled:hover {{"
            f"  background: {PALETTE['accent']};"
            f"}}"
        )
        self.run_btn.clicked.connect(self._rerun_last)
        hl.addWidget(self.run_btn)

        # admin button
        self.admin_btn = QPushButton("⚙")
        self.admin_btn.setFixedSize(30, 30)
        self.admin_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.admin_btn.setToolTip("Open administration panel")
        self.admin_btn.setStyleSheet(
            f"QPushButton {{"
            f"  background: {PALETTE['bg_card']}; color: {PALETTE['text_secondary']}; "
            f"  border: 1px solid {PALETTE['border']}; border-radius: 4px; "
            f"  font-size: 14px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background: {PALETTE['accent_dim']}; color: {PALETTE['text_primary']};"
            f"  border-color: {PALETTE['accent']};"
            f"}}"
        )
        self.admin_btn.clicked.connect(self._open_admin)
        hl.addWidget(self.admin_btn)
        return bar

    def _make_statusbar(self):
        bar = QWidget()
        bar.setFixedHeight(28)
        bar.setStyleSheet(
            f"background: {PALETTE['header_bg']}; "
            f"border-top: 1px solid {PALETTE['border']};"
        )
        hl = QHBoxLayout(bar)
        hl.setContentsMargins(0, 0, 0, 0)
        self.status_lbl = QLabel("  ready")
        self.status_lbl.setObjectName("statusbar")
        hl.addWidget(self.status_lbl)
        hl.addStretch()

        ver = QLabel("v1.0  ")
        ver.setStyleSheet(
            f"font-size: 9px; color: {PALETTE['text_muted']}; "
            "font-family: 'Courier New', monospace;"
        )
        hl.addWidget(ver)
        return bar

    # ── grid population ───────────────────────
    def _populate_grid(self, category: str, search_text: str = ""):
        # remember current state for resize reflow
        self._last_category = category
        self._last_search = search_text

        # clear existing widgets
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # filter by category — each tool has a "category" field in its data
        filtered = list(tools_data.TOOLS)
        if category != "All Tools":
            filtered = [t for t in filtered if t[2] == category]

        # Apply search text filter
        if search_text:
            filtered = [t for t in filtered
                        if (search_text.lower() in t[1].lower()
                            or search_text.lower() in t[2].lower()
                            or search_text.lower() in t[4].lower())]

        # group by category for section headers
        groups: dict[str, list] = {}
        for t in filtered:
            groups.setdefault(t[2], []).append(t)

        COLS = self._cols
        row = 0

        for cat_name, tools in groups.items():
            # section header  (only show category headers when not filtering by search)
            if category == "All Tools" and not search_text:
                lbl = QLabel(cat_name.upper())
                lbl.setObjectName("section_label")
                self.grid_layout.addWidget(lbl, row, 0, 1, COLS)
                row += 1

                sep = QFrame()
                sep.setObjectName("sep")
                sep.setFrameShape(QFrame.HLine)
                self.grid_layout.addWidget(sep, row, 0, 1, COLS)
                row += 1

            for i, t in enumerate(tools):
                tool_dict = {
                    "id": t[0], "label": t[1], "category": t[2],
                    "icon": t[3], "tooltip": t[4], "script": t[5],
                }
                btn = ToolButton(tool_dict)
                btn.clicked.connect(self._on_tool_clicked)
                col = i % COLS
                if col == 0 and i != 0:
                    row += 1
                self.grid_layout.addWidget(btn, row, col)

            row += 1  # gap after group

        # stretch at bottom
        self.grid_layout.setRowStretch(row + 1, 1)

        # cache current column count for resize comparison
        self._last_cols = COLS

    def _on_search(self, text: str):
        """Filter tools by name when search text changes."""
        self._populate_grid(self.combo.currentText(), text.strip())

    # ── admin panel ───────────────────────────
    def _open_admin(self):
        """Open the administration panel to manage tools/categories."""
        dialog = AdminPanel(self)
        dialog.exec_()

        # Reload data after admin changes
        self._refresh_data()

    def _refresh_data(self):
        """Reload TOOLS and CATEGORIES from Library/ and repopulate the grid."""
        from .library_manager import load_categories, _tools_as_tuples

        # Reload mutable objects in-place
        tools_data.CATEGORIES.clear()
        tools_data.CATEGORIES.update(load_categories())
        tools_data.TOOLS.clear()
        tools_data.TOOLS.extend(_tools_as_tuples())

        # Rebuild combo items
        self.combo.blockSignals(True)
        current_cat = self.combo.currentText()
        self.combo.clear()
        for cat in tools_data.CATEGORIES.keys():
            self.combo.addItem(cat)
        idx = self.combo.findText(current_cat)
        if idx >= 0:
            self.combo.setCurrentIndex(idx)
        self.combo.blockSignals(False)

        # Repopulate grid
        self._populate_grid(self.combo.currentText(), self.search_bar.text().strip())

        self.status_lbl.setObjectName("statusbar")
        self.status_lbl.setText("  ✔  Library reloaded")
        self.status_lbl.style().unpolish(self.status_lbl)
        self.status_lbl.style().polish(self.status_lbl)

    # ── actions ───────────────────────────────
    def _on_tool_clicked(self, tool: dict):
        self._last_tool = tool
        self.run_btn.setEnabled(True)
        self._execute(tool)

    def _rerun_last(self):
        if hasattr(self, "_last_tool"):
            self._execute(self._last_tool)

    def _execute(self, tool: dict):
        self.status_lbl.setObjectName("statusbar")
        self.status_lbl.setText(f"  ▶  running: {tool['label']} …")
        self.status_lbl.style().unpolish(self.status_lbl)
        self.status_lbl.style().polish(self.status_lbl)
        QApplication.processEvents()  # flush UI before script runs

        try:
            exec(tool["script"], _EXEC_GLOBALS)
            self.status_lbl.setObjectName("statusbar_ok")
            self.status_lbl.setText(f"  ✔  {tool['label']} — done")
        except Exception as e:
            self.status_lbl.setObjectName("statusbar")
            self.status_lbl.setText(f"  ✖  error: {str(e)[:60]}")

        self.status_lbl.style().unpolish(self.status_lbl)
        self.status_lbl.style().polish(self.status_lbl)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def launch():
    """
    Call inside Houdini:
        import main
        main.launch()

    Or run standalone:
        python main.py
    """
    existing = QApplication.instance()
    if existing:
        win = HoudiniToolsPanel()
        win.show()
        win.raise_()
        win.activateWindow()
        launch._win = win  # prevent GC
        return win
    else:
        app = QApplication(sys.argv)
        win = HoudiniToolsPanel()
        win.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    launch()
