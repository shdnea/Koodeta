"""
tool_button.py
Houdini Tools Panel — ToolButton widget class.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, QTimer, Property
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QCursor

from .stylesheet import PALETTE


class ToolButton(QWidget):
    clicked = Signal(dict)

    def __init__(self, tool_data: dict, parent=None):
        super().__init__(parent)
        self.tool = tool_data
        self.setFixedHeight(100)
        self.setMinimumWidth(80)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip(tool_data["tooltip"])
        self._hovered = False
        self._pressed = False
        self._flash = False
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # icon area
        self.icon_lbl = QLabel(self.tool["icon"], self)
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        self.icon_lbl.setStyleSheet(
            f"font-size: 24px; color: {PALETTE['text_secondary']}; "
            "background: transparent; padding-top: 16px;"
        )

        # name label
        self.name_lbl = QLabel(self.tool["label"], self)
        self.name_lbl.setAlignment(Qt.AlignCenter)
        self.name_lbl.setWordWrap(True)
        self.name_lbl.setStyleSheet(
            f"font-size: 10px; font-family: 'Segoe UI', 'Inter', 'Helvetica Neue', sans-serif; "
            f"font-weight: 600; letter-spacing: 0.3px; color: {PALETTE['text_secondary']}; "
            "background: transparent; padding: 4px 6px;"
        )

        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.name_lbl)
        layout.addStretch()

    # ── painting ──────────────────────────────
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(2, 2, -2, -2)

        if self._flash:
            fill = QColor(PALETTE["accent_dim"])
        elif self._pressed:
            fill = QColor(PALETTE["bg_card_press"])
        elif self._hovered:
            fill = QColor(PALETTE["bg_card_hover"])
        else:
            fill = QColor(PALETTE["bg_card"])

        # card background
        painter.setBrush(QBrush(fill))
        border_col = QColor(PALETTE["border_hover"] if (self._hovered or self._flash)
                            else PALETTE["border"])
        painter.setPen(QPen(border_col, 1))
        painter.drawRoundedRect(r, 6, 6)

        # top accent stripe
        if self._hovered or self._flash:
            stripe = r.adjusted(0, 0, 0, -(r.height() - 3))
            painter.setBrush(QBrush(QColor(PALETTE["accent"])))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(stripe, 3, 3)

        painter.end()

    # ── events ────────────────────────────────
    def enterEvent(self, event):
        self._hovered = True
        self.icon_lbl.setStyleSheet(
            f"font-size: 26px; color: {PALETTE['accent']}; "
            "background: transparent; padding-top: 14px;"
        )
        self.name_lbl.setStyleSheet(
            f"font-size: 10px; font-family: 'Segoe UI', 'Inter', 'Helvetica Neue', sans-serif; "
            f"font-weight: 600; letter-spacing: 0.3px; color: {PALETTE['text_primary']}; "
            "background: transparent; padding: 4px 6px;"
        )
        self.update()

    def leaveEvent(self, event):
        self._hovered = False
        self.icon_lbl.setStyleSheet(
            f"font-size: 24px; color: {PALETTE['text_secondary']}; "
            "background: transparent; padding-top: 16px;"
        )
        self.name_lbl.setStyleSheet(
            f"font-size: 10px; font-family: 'Segoe UI', 'Inter', 'Helvetica Neue', sans-serif; "
            f"font-weight: 600; letter-spacing: 0.3px; color: {PALETTE['text_secondary']}; "
            "background: transparent; padding: 4px 6px;"
        )
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = False
            self._flash = True
            self.update()
            QTimer.singleShot(180, self._end_flash)
            self.clicked.emit(self.tool)

    def _end_flash(self):
        self._flash = False
        self.update()

