"""Logging configuration utilities."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict


def setup_logging(log_file: str | Path, level: int = logging.INFO) -> None:
    """Configure JSON console and file logging."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            record_dict: Dict[str, Any] = {
                "time": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
                "level": record.levelname,
                "name": record.name,
                "message": record.getMessage(),
            }
            if record.exc_info:
                record_dict["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(record_dict)

    formatter: logging.Formatter = JsonFormatter()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[console_handler, file_handler])
