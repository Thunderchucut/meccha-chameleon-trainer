"""User-mode overlay (Qt) used for ESP boxes, crosshair, and debug text."""
from __future__ import annotations

from meccha_trainer.services.config_service import ConfigService
from meccha_trainer.utils.logging import get_logger

log = get_logger(__name__)


class OverlayService:
    def __init__(self, cfg: ConfigService) -> None:
        self.cfg = cfg
        self._app = None
        self._window = None
        self._running = False

    def start(self) -> None:
        try:
            from PySide6.QtWidgets import QApplication
            from meccha_trainer.ui.overlay_window import OverlayWindow
        except ImportError as exc:
            log.error("overlay.import_failed", err=str(exc))
            return
        self._app = QApplication.instance() or QApplication([])
        self._window = OverlayWindow(self.cfg)
        self._window.show()
        self._running = True
        log.info("overlay.started")

    def push_esp(self, boxes: list[dict]) -> None:
        if self._window is not None:
            self._window.set_esp_boxes(boxes)

    def stop(self) -> None:
        self._running = False
        if self._window is not None:
            self._window.close()
            self._window = None
        log.info("overlay.stopped")