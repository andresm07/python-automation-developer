import logging
import logging.config
import re


class SensitiveDataMasker(logging.Filter):
    def __init__(self, patterns=None):
        super().__init__()

        self.patterns = patterns or [
            #! Matches key=value pairs
            (
                r"(?i)(password|passwd|api_key|secret|token)\s*=\s*['\"]?[^\s'\",]+['\"]?",
                r"\1=[KEY-REDACTED]",
            ),
            #! Matches Bearer tokens
            (
                r"(?i)(bearer\s+)[a-zA-Z0-9\-\._~\+\/]+=*",
                r"\1[TOKEN-REDACTED]",
            ),
            #! Matches 16-digit credit card numbers
            (r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[CARD-REDACTED]"),
        ]

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()

        for pattern, replacement in self.patterns:
            message = re.sub(pattern, replacement, message)

        record.msg = message
        record.args = ()

        return True


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "mask_sensitive": {
            "()": SensitiveDataMasker,
        },
    },
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - [%(lineno)d]: %(funcName)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": ["mask_sensitive"],
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "log_masking.log",
            "maxBytes": 10485760,  #! 10 MB
            "backupCount": 5,
            "formatter": "standard",
            "filters": ["mask_sensitive"],
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

logger.info("User login attempt with password=asdlkjasdjaslkdjlasd")
logger.info("Auth header sent: Bearer eyJhdlkajsdlkasjdlkasjd... token")
logger.info("Card used 4242-4242-4242-4242")
