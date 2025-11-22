from flask_sse_with_logs.utils import IngestLogFileState, log, LogLevel, LogQueue, ReadFile


class ParseSIEMLogs:
    def __init__(self, logfile):
        self.siem_logfile  = logfile

    def _get_siem_logs_from_file(self) -> LogQueue:
        read_siem_logfile = ReadFile(self.siem_logfile)
        logqueue = read_siem_logfile._read_file()
        return logqueue
    
    def parselogs_and_store_to_db(self):
        
        logrecords = set()

        logqueue = self._get_siem_logs_from_file()

        while logqueue.is_empty() == False:
            current_log = logqueue.dequeue()

            print(current_log)