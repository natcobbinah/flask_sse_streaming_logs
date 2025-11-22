from flask_sse_with_logs.config import db
from sqlalchemy.orm import Mapped, mapped_column 
from typing import Optional

class SIEMLogsDBtable(db.Model):
    __tablename__ = "siemlogs_dbtable"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp : Mapped[str]
    event_type: Mapped[str]
    message: Mapped[str]
    severity: Mapped[str]
    loglevel: Mapped[str]


class SIEMLogsFileDBProperties(db.Model):
    __tablename__ = "siemlogs_fileproperties"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_size : Mapped[Optional[int]]  = mapped_column(nullable=True)
    logfile_status: Mapped[str]