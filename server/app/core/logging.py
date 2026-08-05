"""Structured logging configuration using structlog.

Outputs:
  - Console: human-readable colored logs
  - logs/robot.log: JSON structured logs for all modules
"""

import logging
import logging.handlers
import sys
from pathlib import Path

import structlog


def configure_logging(log_level: str = "INFO", log_dir: str = "logs") -> None:
    """Configure structlog + stdlib logging with file and console output."""

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    level = getattr(logging, log_level.upper(), logging.INFO)

    # ── Stdlib handlers ───────────────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=f"{log_dir}/robot.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[console_handler, file_handler],
        format="%(message)s",
    )

    # Silence noisy third-party loggers
    for lib in ("uvicorn.access", "httpx", "httpcore", "groq"):
        logging.getLogger(lib).setLevel(logging.WARNING)

    # ── Structlog processors ──────────────────────────────────────────────────
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.processors.StackInfoRenderer(),
    ]

    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a named logger."""
    return structlog.get_logger(name)
