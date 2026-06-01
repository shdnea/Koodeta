"""
admin_panel.py
Acnologia Administration Panel — add, edit, delete tools & categories.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QSplitter,
    QGroupBox, QWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .stylesheet import PALETTE, STYLESHEET
from .library_manager import (
    load_tools, save_tool, delete_tool,
    load_categories, save_categories, add_tool,
)


class AdminPanel(QDialog):
    """Dialog for managing tools and categories."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acnologia — Administration")
        self.setMinimumSize(720, 520)
        self.resize(800, 600)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()
        self._refresh_tool_list()
        self._refresh_category_list()

    # ── UI build ──────────────────────────────
    def _build_ui(self):
        root = QWidget(self)
        root.setObjectName("root")
        root.setStyleSheet(f"background: {PALETTE['bg_deep']};")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(44)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(16, 0, 16, 0)
        title = QLabel("⚙  ADMINISTRATION")
        title.setObjectName("title")
        title.setStyleSheet("font-size: 11px;")
        hl.addWidget(title)
        hl.addStretch()
        outer.addWidget(header)

        # Splitter: left = tool list, right = editor
        splitter = QSplitter(Qt.Horizontal)

        # ── Left panel: tool list ──
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 8, 6, 8)

        left_layout.addWidget(QLabel("TOOLS"))
        self.tool_list = QListWidget()
        self.tool_list.setStyleSheet(
            f"QListWidget {{"
            f"  background: {PALETTE['bg_card']}; color: {PALETTE['text_primary']};"
            f"  border: 1px solid {PALETTE['border']}; border-radius: 4px;"
            f"  font-size: 11px; font-family: 'Courier New', monospace;"
            f"}}"
            f"QListWidget::item:selected {{"
            f"  background: {PALETTE['accent_dim']}; color: {PALETTE['text_primary']};"
            f"}}"
            f"QListWidget::item:hover {{"
            f"  background: {PALETTE['bg_card_hover']};"
            f"}}"
        )
        self.tool_list.currentRowChanged.connect(self._on_tool_selected)
        left_layout.addWidget(self.tool_list)

        # Tool list buttons
        btn_row = QHBoxLayout()
        self.btn_add = QPushButton("+  ADD")
        self.btn_add.setStyleSheet(self._btn_style(PALETTE["success"]))
        self.btn_add.clicked.connect(self._add_tool)

        self.btn_delete = QPushButton("✕  DELETE")
        self.btn_delete.setStyleSheet(self._btn_style(PALETTE["accent_dim"]))
        self.btn_delete.clicked.connect(self._delete_tool)

        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_delete)
        left_layout.addLayout(btn_row)

        splitter.addWidget(left_panel)

        # ── Right panel: editor ──
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(6, 8, 12, 8)

        # Tool editor form
        editor_group = QGroupBox("Tool Editor")
        editor_group.setStyleSheet(
            f"QGroupBox {{"
            f"  color: {PALETTE['text_primary']}; font-size: 11px;"
            f"  font-family: 'Courier New', monospace;"
            f"  border: 1px solid {PALETTE['border']};"
            f"  border-radius: 4px; margin-top: 12px; padding-top: 16px;"
            f"}}"
        )
        form = QFormLayout(editor_group)
        form.setSpacing(6)

        self.edit_id = QLineEdit()
        self.edit_id.setReadOnly(True)
        self.edit_id.setStyleSheet(self._input_style())

        self.edit_label = QLineEdit()
        self.edit_label.setStyleSheet(self._input_style())

        self.edit_icon = QLineEdit(maxLength=4)
        self.edit_icon.setStyleSheet(self._input_style())

        self.edit_category = QComboBox()
        self.edit_category.setStyleSheet(
            f"QComboBox {{"
            f"  background: {PALETTE['bg_card']}; color: {PALETTE['text_primary']};"
            f"  border: 1px solid {PALETTE['border']}; border-radius: 4px;"
            f"  padding: 4px 8px; font-size: 11px;"
            f"}}"
            f"QComboBox:hover {{ border-color: {PALETTE['accent']}; }}"
            f"QComboBox QAbstractItemView {{"
            f"  background: {PALETTE['bg_panel']}; color: {PALETTE['text_primary']};"
            f"  border: 1px solid {PALETTE['border']};"
            f"  selection-background-color: {PALETTE['accent_dim']};"
            f"  font-size: 11px;"
            f"}}"
        )

        self.edit_tooltip = QLineEdit()
        self.edit_tooltip.setStyleSheet(self._input_style())

        self.edit_script = QTextEdit()
        self.edit_script.setMinimumHeight(140)
        self.edit_script.setStyleSheet(
            f"QTextEdit {{"
            f"  background: {PALETTE['bg_card']}; color: {PALETTE['text_primary']};"
            f"  border: 1px solid {PALETTE['border']}; border-radius: 4px;"
            f"  font-size: 11px; font-family: 'Courier New', monospace;"
            f"  padding: 6px;"
            f"}}"
            f"QTextEdit:focus {{ border-color: {PALETTE['accent']}; }}"
        )

        form.addRow("ID:", self.edit_id)
        form.addRow("Label:", self.edit_label)
        form.addRow("Icon:", self.edit_icon)
        form.addRow("Category:", self.edit_category)
        form.addRow("Tooltip:", self.edit_tooltip)
        form.addRow("Script:", self.edit_script)

        right_layout.addWidget(editor_group)

        # Save / Cancel buttons
        action_row = QHBoxLayout()
        self.btn_save = QPushButton("💾  SAVE")
        self.btn_save.setStyleSheet(self._btn_style(PALETTE["accent"]))
        self.btn_save.clicked.connect(self._save_tool)

        self.btn_cancel = QPushButton("✕  CANCEL")
        self.btn_cancel.setStyleSheet(self._btn_style(PALETTE["text_secondary"]))
        self.btn_cancel.clicked.connect(self._clear_form)

        action_row.addStretch()
        action_row.addWidget(self.btn_save)
        action_row.addWidget(self.btn_cancel)
        right_layout.addLayout(action_row)

        right_layout.addStretch()

        # ── Category manager section ──
        cat_group = QGroupBox("Category Manager")
        cat_group.setStyleSheet(
            f"QGroupBox {{"
            f"  color: {PALETTE['text_primary']}; font-size: 11px;"
            f"  font-family: 'Courier New', monospace;"
            f"  border: 1px solid {PALETTE['border']};"
            f"  border-radius: 4px; margin-top: 12px; padding-top: 16px;"
            f"}}"
        )
        cat_layout = QVBoxLayout(cat_group)

        cat_inner_row = QHBoxLayout()
        self.cat_list = QListWidget()
        self.cat_list.setStyleSheet(self.tool_list.styleSheet())
        self.cat_list.setMaximumHeight(100)

        self.cat_edit = QLineEdit()
        self.cat_edit.setPlaceholderText("New category name")
        self.cat_edit.setStyleSheet(self._input_style())

        cat_btn_row = QVBoxLayout()
        self.btn_cat_add = QPushButton("+ ADD")
        self.btn_cat_add.setStyleSheet(self._btn_style(PALETTE["success"]))
        self.btn_cat_add.clicked.connect(self._add_category)

        self.btn_cat_delete = QPushButton("✕ REMOVE")
        self.btn_cat_delete.setStyleSheet(self._btn_style(PALETTE["accent_dim"]))
        self.btn_cat_delete.clicked.connect(self._delete_category)

        cat_btn_row.addWidget(self.btn_cat_add)
        cat_btn_row.addWidget(self.btn_cat_delete)

        cat_inner_row.addWidget(self.cat_list, 1)
        cat_inner_row.addWidget(self.cat_edit, 1)
        cat_inner_row.addLayout(cat_btn_row)
        cat_layout.addLayout(cat_inner_row)

        right_layout.addWidget(cat_group)

        splitter.addWidget(right_panel)
        splitter.setSizes([240, 480])
        outer.addWidget(splitter, 1)

    # ── helpers ───────────────────────────────
    def _input_style(self):
        return (
            f"background: {PALETTE['bg_card']}; color: {PALETTE['text_primary']};"
            f"border: 1px solid {PALETTE['border']}; border-radius: 4px;"
            f"padding: 4px 8px; font-size: 11px;"
            f"font-family: 'Courier New', monospace;"
        )

    def _btn_style(self, color: str):
        return (
            f"QPushButton {{"
            f"  background: {PALETTE['bg_card']}; color: {PALETTE['text_primary']};"
            f"  border: 1px solid {color}; border-radius: 4px;"
            f"  padding: 6px 14px; font-size: 10px;"
            f"  font-family: 'Courier New', monospace;"
            f"  letter-spacing: 1px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background: {color};"
            f"}}"
            f"QPushButton:pressed {{"
            f"  background: {PALETTE['accent_dim']};"
            f"}}"
        )

    def _refresh_tool_list(self):
        self.tool_list.blockSignals(True)
        self.tool_list.clear()
        for t in load_tools():
            item = QListWidgetItem(f"#{t['id']:03d}  {t['label']}")
            item.setData(Qt.UserRole, t["id"])
            self.tool_list.addItem(item)
        self.tool_list.blockSignals(False)

    def _refresh_category_list(self):
        self.cat_list.clear()
        cats = load_categories()
        for name in cats:
            if name != "All Tools":
                self.cat_list.addItem(name)
        # Refresh category combo in editor
        current = self.edit_category.currentText()
        self.edit_category.clear()
        self.edit_category.addItems([k for k in cats if k != "All Tools"])
        if current:
            idx = self.edit_category.findText(current)
            if idx >= 0:
                self.edit_category.setCurrentIndex(idx)

    # ── form actions ─────────────────────────
    def _clear_form(self):
        self.edit_id.clear()
        self.edit_label.clear()
        self.edit_icon.clear()
        self.edit_tooltip.clear()
        self.edit_script.clear()
        if self.edit_category.count():
            self.edit_category.setCurrentIndex(0)

    def _on_tool_selected(self, row: int):
        if row < 0:
            return
        item = self.tool_list.item(row)
        tool_id = item.data(Qt.UserRole)
        tools = load_tools()
        for t in tools:
            if t["id"] == tool_id:
                self.edit_id.setText(str(t["id"]))
                self.edit_label.setText(t.get("label", ""))
                self.edit_icon.setText(t.get("icon", ""))
                self.edit_tooltip.setText(t.get("tooltip", ""))
                self.edit_script.setPlainText(t.get("script", ""))
                idx = self.edit_category.findText(t.get("category", ""))
                if idx >= 0:
                    self.edit_category.setCurrentIndex(idx)
                return

    def _add_tool(self):
        from .library_manager import _next_id
        new_id = _next_id()
        new_tool = {
            "id": new_id,
            "label": "New Tool",
            "category": self.edit_category.currentText() if self.edit_category.count() else "General",
            "icon": "●",
            "tooltip": "Description",
            "script": "import hou\nprint('Hello')",
        }
        save_tool(new_tool)
        self._refresh_tool_list()
        # Select the new item
        for i in range(self.tool_list.count()):
            if self.tool_list.item(i).data(Qt.UserRole) == new_id:
                self.tool_list.setCurrentRow(i)
                break

    def _save_tool(self):
        try:
            tool_id = int(self.edit_id.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid ID", "No tool selected to save.")
            return

        label = self.edit_label.text().strip()
        if not label:
            QMessageBox.warning(self, "Missing Label", "Tool label cannot be empty.")
            return

        updated = {
            "id": tool_id,
            "label": label,
            "category": self.edit_category.currentText(),
            "icon": self.edit_icon.text().strip() or "●",
            "tooltip": self.edit_tooltip.text().strip(),
            "script": self.edit_script.toPlainText(),
        }
        save_tool(updated)
        self._refresh_tool_list()
        # Keep selection
        for i in range(self.tool_list.count()):
            if self.tool_list.item(i).data(Qt.UserRole) == tool_id:
                self.tool_list.setCurrentRow(i)
                break

    def _delete_tool(self):
        item = self.tool_list.currentItem()
        if not item:
            return
        tool_id = item.data(Qt.UserRole)
        label = item.text()
        confirm = QMessageBox.question(
            self, "Delete Tool",
            f'Delete "{label}" permanently?',
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            delete_tool(tool_id)
            self._refresh_tool_list()
            self._clear_form()

    # ── category actions ─────────────────────
    def _add_category(self):
        name = self.cat_edit.text().strip()
        if not name:
            return
        cats = load_categories()
        if name in cats:
            QMessageBox.warning(self, "Duplicate", f'Category "{name}" already exists.')
            return
        cats[name] = []
        save_categories(cats)
        self.cat_edit.clear()
        self._refresh_category_list()

    def _delete_category(self):
        item = self.cat_list.currentItem()
        if not item:
            return
        name = item.text()
        confirm = QMessageBox.question(
            self, "Delete Category",
            f'Delete category "{name}"? Tools in this category will remain but become uncategorised.',
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            cats = load_categories()
            if name in cats:
                del cats[name]
                save_categories(cats)
            self._refresh_category_list()
