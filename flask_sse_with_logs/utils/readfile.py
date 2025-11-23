from dataclasses import dataclass
from typing import Union
from .Logqueue import LogQueue
from .logger import log, LogLevel
import string

@dataclass
class ReadFile:
    _filepath: str 

    def _read_file(self) -> Union[LogQueue, str]:
        log(type=LogLevel.INFO, message='Read logs in SIEM directory')

        logqueue = LogQueue() 

        filepath = self._filepath

        try:
            with open(filepath) as f:
                lines = f.readlines()

                for line in lines:
                    line = line.strip() 

                    if line in string.whitespace:
                        continue
                    logqueue.enqueue(line)
            
            log(type=LogLevel.INFO, message='Read logs in SIEM directory completed')

            return logqueue 
        except UnicodeDecodeError:
            log(type=LogLevel.INFO, message='Invalid file')
        except OSError:
            log(type=LogLevel.INFO, message='File not found')
