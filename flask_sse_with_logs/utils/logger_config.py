from collections import OrderedDict

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s in %(module)s: %(message)s",
        },
        "standard": {
            "class": "jsonformatter.JsonFormatter",
            "format": OrderedDict(
                [
                    ("Time", "asctime"),
                    ("Loglevel", "levelname"),
                    ("Filename", "appfilename"),
                    ("Component", "component"),
                    ("Event", "event"),
                    ("FunctionName", "function_name"),
                    ("Fileline", "fileline"),
                    ("CorrelationID", "correlation_id"),
                    ("Reason", "reason"),
                    ("Message", "message"),
                    ("MessageData", "message_data"),
                    #("Name", "name"),
                    #("Levelno", "levelno"),
                    #("Module", "module"),
                    #("Lineno", "lineno"),
                    #("FuncName", "funcName"),
                    #("Created", "created"),
                    #("Msecs", "msecs"),
                    #("RelativeCreated", "relativeCreated"),
                    #("Thread", "thread"),
                    #("ThreadName", "threadName"),
                    #("Process", "process"),
                ]
            ),
        },
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "standard",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "flask_sse_with_logs.logs",
            "formatter": "standard",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "flask_sse_with_logs_logger": {"level": "DEBUG", "handlers": ["wsgi", "file_handler"]},
    },
}
