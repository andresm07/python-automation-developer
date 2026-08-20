import json
import logging
import logging.config
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "source": {
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
            },
            "process_id": record.process,
            "thread_id": record.thread,
        }

        #! Include exception stack traces if an error occurred
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        #! Merge custom contextual attributes passed via extra={}
        #! ie: logger.info("User logged in", extra={"user_id": 12345})
        standard_attributes = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "thread",
            "threadName",
            "processName",
            "process",
        }

        extra_fields = {
            k: v
            for k, v in record.__dict__.items()
            if k not in standard_attributes
        }

        if extra_fields:
            log_payload["extra"] = extra_fields

        return json.dumps(log_payload)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - [%(lineno)d]: %(funcName)s - %(message)s",
        },
        "json": {
            "()": JSONFormatter,
        },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "splunk.log",
            "maxBytes": 10485760,  #! 10 MB
            "backupCount": 5,
            "formatter": "json",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "DEBUG",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("custom_logger")

logger.info(
    "Logger health check",
    extra={
        "status_code": 200,
        "latency_ms": 12.4,
        "description": "Logger is working!",
    },
)
