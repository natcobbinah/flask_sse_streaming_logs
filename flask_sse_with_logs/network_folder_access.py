import glob 
import os 
from sqlalchemy import select, update 
from flask_sse_with_logs.models import SIEMLogsFileDBProperties
from flask_sse_with_logs.utils import IngestLogFileState, log, LogLevel, LogQueue
from flask_sse_with_logs.config import db
from flask_sse_with_logs.LogParser import ParseSIEMLogs



class SIEMNetworkFolderAccess:
    """
    SIEMNetworkFolderAccess class 
        Contains methods for ingesting logfiles contained in SIEM network folder
    """

    def __init__(self, siem_logfile_access_path):
        self.siem_logfile = siem_logfile_access_path

    def _get_logfiles_from_siem_folder_directory(self) -> LogQueue:

        log(type=LogLevel.INFO, message='Accessing logs in SIEM directory')

        print(self.siem_logfile)

        logfiles_path = glob.glob(self.siem_logfile)
        print(logfiles_path)

        siem_logfilespath_queue = LogQueue()

        # assuming we are only interested in a single logfile contained in the SIEM directory and not the others
        with os.scandir(logfiles_path[0]) as it:
            for siem_event_log in it:
                if siem_event_log.name == ('siem_events.log') and siem_event_log.is_file():
                    logfile_path = f"{self.siem_logfile}/{siem_event_log.name}"
                    siem_logfilespath_queue.enqueue(logfile_path)
        
        log(type=LogLevel.INFO, message='Interested SIEM Logfile path accessed successfully')
        
        return siem_logfilespath_queue
    
    def parse_and_process_ingested_logfile(self) -> None: 
        
        log(type=LogLevel.INFO, message='Start: Parsing and processing logfile from SIEM directory')


        logfiles_path_queue = self._get_logfiles_from_siem_folder_directory()

        while not logfiles_path_queue.is_empty():
            current_logfile = logfiles_path_queue.dequeue()

            print(f'currentlogfile {current_logfile}')

            self._store_siem_logfile_properties_to_db(current_logfile)

            current_logfile_status = self._get_siem_logfile_size_status()

            if (
                current_logfile_status 
                == IngestLogFileState.NEW_LOGFILE_PROPERTIES.value
            ):
                log(type=LogLevel.INFO, message='New logfile properties (file size) inserted into SIEMLogsFileDBProperties table')

                self._parse_siem_logs(current_logfile)
            
            elif (
                current_logfile_status 
                == IngestLogFileState.UPDATED_LOGFILE_PROPERTIES.value
            ):
                log(type=LogLevel.INFO, message='logfile properties (file size) has been updated in SIEMLogsFileDBProperties table')

                self._parse_siem_logs(current_logfile)

            elif  (
                current_logfile_status 
                == IngestLogFileState.NOT_UPDATED_LOGFILE_PROPERTIES.value
            ):
                log(type=LogLevel.INFO, message='logfile properties (file size) has not been updated in SIEMLogsFileDBProperties table')

                return 

    
    def _store_siem_logfile_properties_to_db(self, current_logfile) -> None: 

        current_logfile_statresults = os.stat(current_logfile)


        # only (siem_events.log) file is ingested and processed for now, so we assume its id will be 1,
        # if the others will be ingested as well, they can be assigned with different ids
        stmt = select(SIEMLogsFileDBProperties).where(
            SIEMLogsFileDBProperties.id == 1
        )

        """
        model structure of SIEMLogsFileDBProperties, contained in (models)
        """

        if db.session.execute(stmt).first() is None:
            siem_logfile_properties = SIEMLogsFileDBProperties(
                id = 1,
                file_size=current_logfile_statresults.st_size,
                logfile_status=IngestLogFileState.NEW_LOGFILE_PROPERTIES.value
            )
            db.session.add(siem_logfile_properties)
            db.session.commit()
        
        else:
            # get current (siem_events.log) file size and compare it to the previously processed logfile properties stored in 
            # SIEMLogsFileDBProperties table
            siem_event_logfile_size_from_db = select(SIEMLogsFileDBProperties).where(
                SIEMLogsFileDBProperties.id == 1
            )

            siem_event_logfile_size_from_db_result = db.session.execute(siem_event_logfile_size_from_db).scalar()

            if (
                siem_event_logfile_size_from_db_result.file_size
                != current_logfile_statresults.st_size
            ):
                # if there's been an update to the (siem_event.log) file  update the file size, and its status in the table
                stmt = (
                    update(SIEMLogsFileDBProperties)
                    .where(SIEMLogsFileDBProperties.id == 1)
                    .values(
                        (
                            SIEMLogsFileDBProperties.id,
                            current_logfile_statresults.st_size,
                            IngestLogFileState.UPDATED_LOGFILE_PROPERTIES.value
                        )
                    )
                )        

                db.session.execute(stmt) 
                db.session.commit()
            
            else:
                # if there's been no change to the (siem_event.log) file
                stmt = (
                    update(SIEMLogsFileDBProperties)
                    .where(SIEMLogsFileDBProperties.id == 1)
                    .values(
                        (
                            SIEMLogsFileDBProperties.id,
                            current_logfile_statresults.st_size,
                            IngestLogFileState.NOT_UPDATED_LOGFILE_PROPERTIES.value
                        )
                    )
                )        

                db.session.execute(stmt) 
                db.session.commit()


    def _get_siem_logfile_size_status(self) -> str:
        stmt = select(SIEMLogsFileDBProperties).where(
            SIEMLogsFileDBProperties.id == 1
        )

        # indicates the first time a new (siem_event.log) file has been inserted into the database table
        # thus we connect to the SIEM_folder and , ingest and process the logfile
        if(
            db.session.execute(stmt).scalar().logfile_status
            == IngestLogFileState.NEW_LOGFILE_PROPERTIES.value
        ):
            return IngestLogFileState.NEW_LOGFILE_PROPERTIES.value
        
        # indicates, the (siem_event.log) file has been updated, thus we connect to SIEM_folder, ingest and process the logfile
        elif(
            db.session.execute(stmt).scalar().logfile_status
            == IngestLogFileState.UPDATED_LOGFILE_PROPERTIES.value
        ):
            return  IngestLogFileState.NEW_LOGFILE_PROPERTIES.value
        
        # indicates no update has been performed, thus no ingestion and processing of the logfile is performed
        elif(
            db.session.execute(stmt).scalar().logfile_status
            == IngestLogFileState.NOT_UPDATED_LOGFILE_PROPERTIES.value
        ):
            return  IngestLogFileState.NOT_UPDATED_LOGFILE_PROPERTIES.value
    
    def _parse_siem_logs(self, logfile):
        logparse_instance = ParseSIEMLogs(
            logfile
        )
        logparse_instance.parselogs_and_store_to_db()
        
