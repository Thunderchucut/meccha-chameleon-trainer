"""Frameless transparent overlay window for ESP and crosshair."""
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from meccha_trainer.services.config_service import ConfigService


class OverlayWindow(QWidget):
    def __init__(self, cfg: ConfigService) -> None:
        super().__init__(None, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
                         | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.cfg = cfg
        self._esp_boxes: list[dict] = []
        self._crosshair = cfg.get("overlay.crosshair", True)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(16)

    def set_esp_boxes(self, boxes: list[dict]) -> None:
        self._esp_boxes = boxes

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(0, 255, 140, 220), 1.5)
        painter.setPen(pen)
        for box in self._esp_boxes:
            painter.drawRect(box["x"], box["y"], box["w"], box["h"])
            if label := box.get("label"):
                painter.drawText(box["x"], box["y"] - 4, label)
        if self._crosshair:
            cx, cy = self.width() // 2, self.height() // 2
            painter.drawLine(cx - 8, cy, cx + 8, cy)
            painter.drawLine(cx, cy - 8, cx, cy + 8)