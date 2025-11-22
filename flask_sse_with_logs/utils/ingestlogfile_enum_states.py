from enum import Enum

class IngestLogFileState(Enum):

    """
    Provides the various states, after storing the network logfile properties in LogServerDBFileProperties

    With these properties, automatic ingestion of network logfile is controlled by either
    re-running the ingestion of the logfile again after a specific time interval or not
    if the network logifle size has changed, comparing it to its earlier file sized stored in the database
    """

    NEW_LOGFILE_PROPERTIES = "NEW"
    UPDATED_LOGFILE_PROPERTIES = "UPDATED"
    NOT_UPDATED_LOGFILE_PROPERTIES = "NOT_UPDATED"