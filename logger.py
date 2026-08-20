import logging.config


class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        return "password" not in record.getMessage().lower()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - [%(lineno)d]: %(funcName)s - %(message)s",
        },
    },
    #! FILTERS: Determine which log records to output
    "filters": {
        "block_sensitive": {"()": SensitiveDataFilter},
    },
    #! HANDLERS: Destinations for our log records
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10485760,  #! 10 MB
            "backupCount": 5,
            "formatter": "standard",
            "filters": ["block_sensitive"],
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "filters": ["block_sensitive"],
        },
    },
    "loggers": {
        "app.core": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            #! ATTACH FILTERS
            "filters": ["block_sensitive"],
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "DEBUG",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
