from flask_sse_with_logs.utils import IngestLogFileState, log, LogLevel, LogQueue, ReadFile
from flask_sse_with_logs.config import db
from flask_sse_with_logs.models import SIEMLogsDBtable
import json

class ParseSIEMLogs:
    def __init__(self, logfile):
        self.siem_logfile  = logfile

    def _get_siem_logs_from_file(self) -> LogQueue:
        read_siem_logfile = ReadFile(self.siem_logfile)
        logqueue = read_siem_logfile._read_file()
        return logqueue
    
    def parselogs_and_store_to_db(self):

        log(type=LogLevel.INFO, message='Processing and storing SIEM logs to database started')

        logrecords = set()

        logqueue = self._get_siem_logs_from_file()

        while logqueue.is_empty() == False:
            current_log = logqueue.dequeue()

            # already each log record is in JSON format
            logrecords.add(current_log)

        # store logrecords to database
        for logrecord in logrecords:
            logrecord_to_json = json.loads(logrecord)

            siem_log_dbrecord = SIEMLogsDBtable(
                timestamp=logrecord_to_json["timestamp"],
                event_type=logrecord_to_json["event_type"],
                message=logrecord_to_json["message"],
                severity=logrecord_to_json["severity"],
                loglevel=logrecord_to_json["loglevel"]
            )
            db.session.add(siem_log_dbrecord)
        db.session.commit()

        log(type=LogLevel.INFO, message='All parsed SIEM logs have been stored to database successfully')