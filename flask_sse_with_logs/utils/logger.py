from enum import Enum 
import logging 
from typing import Optional, List, Union, Dict

logger = logging.getLogger('flask_sse_with_logs_logger')

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    EXCEPTION = "EXCEPTION"
    

def log(*,
        type: LogLevel,
        component: Optional[str] = None,
        event: Optional[str] = None,
        filename: Optional[str] = None,
        function_name: Optional[str] = None,
        fileline: Optional[int] = None,
        correlation_id: Optional[str] = None,
        message: Optional[str] = None,
        message_data: Optional[Union[Dict, List, str, set, tuple]] = None,
        reason: Optional[str] = None,
       ) -> None:
    
    # Prepare the extra context for logging
    extra_context = {
        'component': component,
        'event': event,
        'appfilename': filename,
        'function_name': function_name,
        'fileline': fileline,
        'correlation_id': correlation_id,
        'reason': reason,
        'message_data': message_data
    }

    # Log the message based on the log level
    # The `extra` parameter is used to pass additional context to the logger. 
    # This ensures that the additional fields (`component`, `event`, etc.) are included in the log record.
    if type == LogLevel.DEBUG:
        logger.debug(message, extra=extra_context)
    elif type == LogLevel.INFO:
        logger.info(message, extra=extra_context)
    elif type == LogLevel.WARNING:
        logger.warning(message, extra=extra_context)
    elif type == LogLevel.ERROR:
        logger.error(message, extra=extra_context)
    elif type == LogLevel.CRITICAL:
        logger.critical(message, extra=extra_context)
    elif type == LogLevel.EXCEPTION:
        logger.exception(message, extra=extra_context)
