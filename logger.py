import logging.config


class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        return "password" not in record.getMessage().lower()


"""
Logger Name -> comes from whatever string you pass to logging.getLogger(name). You can control completely, but Python provides strong standard conventions to keep loggers organized.

CASE 1: logging.getLogger(__name__) - Standard Best Practice
>> When you pass __name__, the logger name automatically matches the current module's path in you Python package structure
>> For example, my_script/src/database/connection.py -> __name__ will evaluate to "my_script.src.database.connection"
>> Other example, in the main script __name__ will evaluate to "__main__"

CASE 2: Explicit Custom String
logger = logging.getLogger("automation_script_logger")
>> Name will resolve to "automation_script_logger"

CASE 3: Default/Root Logger
logging.getLogger()
>> Name will resolve to "root"

To check the logger name, we can do

logger = logging.getLogger(__name__)
print(logger.name)

------------------------------------

logging.Filter("app.core")

Acts as a department 'security gate'. It filters log records based strictly on logger hierarchy names using dot notation (ie: app.core.ui).

When initialized as logging.Filter("app.core"), Python checks every incoming LogRecord using two rules:

1. Exact Match: Is the record's logger name exactly app.core?
2. Child Match: Does the record's logger name start with app.core.*

logger = logging.getLogger("app.src")

app.src.credit_scorecard #* ALLOWED
app.src.filename #* ALLOWED

app.tests #! BLOCKED
app.api #! BLOCKED
app.labs #! BLOCKED

"""


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
            #! When propagate is set to true (default), an event logged at a child level automatically bubbles up the hierarchy to parent loggers so their handlers can process the log record as well
            #! Set propagate to false on a custom logger whenever you want to give it its own dedicated handlers and want to isolate it, stopping log events from traveling further up the chain to root or parent handlers
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
