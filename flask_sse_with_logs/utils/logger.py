from enum import Enum 
import logging 

logger = logging.getLogger('flask_sse_with_logs_logger')

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    EXCEPTION = "EXCEPTION"
    


def log(*, type=LogLevel, message:any) -> None:
    if type == LogLevel.DEBUG:
        logger.debug(message)
    elif type == LogLevel.INFO:
        logger.info(message)
    elif type == LogLevel.WARNING:
        logger.warning(message)
    elif type == LogLevel.ERROR:
        logger.error(message)
    elif type == LogLevel.CRITICAL:
        logger.critical(message)
    elif type == LogLevel.EXCEPTION:
        logger.exception(message)