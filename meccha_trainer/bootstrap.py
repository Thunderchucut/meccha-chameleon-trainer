"""Entry point for the MECCHA CHAMELEON Trainer."""
from __future__ import annotations

import argparse
import sys

from meccha_trainer.core.host import TrainerHost
from meccha_trainer.core.registry import PluginRegistry
from meccha_trainer.core.loader import PluginLoader
from meccha_trainer.services.config_service import ConfigService
from meccha_trainer.utils.logging import configure_logging, get_logger


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="meccha-trainer")
    p.add_argument("--dry-run", action="store_true", help="load plugins but do not attach")
    p.add_argument("--config", default="config/default.yaml")
    p.add_argument("--plugin", action="append", default=[], help="force-load plugin by name")
    p.add_argument("--no-overlay", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging()
    log = get_logger(__name__)
    log.info("trainer.start", dry_run=args.dry_run)

    cfg = ConfigService.load(args.config)
    registry = PluginRegistry()
    loader = PluginLoader(registry, cfg)
    loader.discover()

    for name in args.plugin:
        loader.force_enable(name)

    host = TrainerHost(registry, cfg, dry_run=args.dry_run,
                       overlay_enabled=not args.no_overlay)
    try:
        host.run()
    except KeyboardInterrupt:
        log.info("trainer.interrupt")
    finally:
        host.shutdown()
    return 0