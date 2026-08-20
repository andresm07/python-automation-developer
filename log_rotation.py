"""
! --- LOG ROTATIONS ---

RotatingFileHandler

1. It can happen automatically when the max bytes threshold is met
app.log -> app.log.1 -> app.log.2 -> app.log.n

"""

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("rotating_logger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("log_rotation.log", maxBytes=100, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

for i in range(100):
    logger.info(
        f"This is log line number {i} to fill space and trigger log rotation."
    )

"""
! --- LOG ROTATIONS ---

TimedRotatingFileHandler

Time-based log rotation rotates logs automatically at specific time intervals

when
> "S" seconds
> "M" minutes
> "H" hours
> "D" days
> "midnight"
> "W0-W6" week days Monday -> W0, W6 -> Sunday

"""

import logging.config
import os
from datetime import datetime

run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_directory = os.path.join("logs", run_timestamp)

os.makedirs(log_directory, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - [%(lineno)d]: %(funcName)s - %(message)s",
        },
    },
    "handlers": {
        "daily_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(log_directory, "app.log"),
            "when": "midnight",
            "interval": 1,  #! Every day at midnight
            "backupCount": 14,  #! Keep 14 days of logs
            "encoding": "utf-8",
            "formatter": "standard",
            "utc": True,  #! Use UTC for rotation calculations
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["daily_file", "console"],
        "level": "DEBUG",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

logger.info("Application Starting Up...")
