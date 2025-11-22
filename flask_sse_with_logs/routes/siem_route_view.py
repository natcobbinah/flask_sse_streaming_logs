from flask import (
    Blueprint, render_template, request, jsonify, Response, stream_with_context
)
from flask_sse_with_logs.models import (
    SIEMLogsDBtable,
    SIEMLogsFileDBProperties
)
from flask_sse_with_logs.network_folder_access import SIEMNetworkFolderAccess
from flask_sse_with_logs.utils import log, LogLevel
from .default_route_response import default_no_available_data_response
from sqlalchemy import or_, select, func
from flask_sse_with_logs.config import db
import json
import time 


siem_route_view_bp = Blueprint("siem_route", __name__)

INGESTING_STATUS = "COMPLETED"
SIEM_LOGS_DIRECTORY ='SIEM_logs'
SERVER_SENT_EVENT_STREAM_CONTENT_TYPE = "text/event-stream"
SIEM_HOMEPAGE = 'siem_homepage.html'

@siem_route_view_bp.route("/siem_logs", methods=["GET"])
def siem_logs_homepage() -> str:
    print("siem_logs_homepage called")
    log(type=LogLevel.INFO, message="SIEM application homepage")

    return render_template(
        SIEM_HOMEPAGE
    )


@siem_route_view_bp.route("/ingesting_and_processing_siem_logs", methods=["GET"])
def auto_refresh_siemlogs():
    print("auto_refresh_siemlogs called")
    """
    stream_with_context is wrapped around generator function in order to be able
    to access request and app bound context information
    """
    return Response(
        stream_with_context(autofetch_siem_logs_stream()),
        content_type=SERVER_SENT_EVENT_STREAM_CONTENT_TYPE,
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


def autofetch_siem_logs_stream():
    print("autofetch_siem_logs_stream called")
    while True:
        if db.session.query(SIEMLogsDBtable).count() > 0:
            # check if SIEMLogsDBtable has already been populated previously
            # if so wait 1mins before fetching logfile from SIEM_logs directory to parse
            # and process updated logfile and return records to frontend datatable
            time.sleep(60)

            logfile_processing_status = ingest_and_process_logfiles_from_siem_dir()

            if logfile_processing_status == INGESTING_STATUS:
                info = json.dumps({"message": "Completed"})
                yield "data: {}\n\n".format(info)
            else:
                logfile_processing_status = ingest_and_process_logfiles_from_siem_dir()

                if logfile_processing_status == INGESTING_STATUS:
                    info = json.dumps({"message": "Completed"})
                    yield "data: {}\n\n".format(info)
                    # wait 1 min before fetching from siem directory again
                    time.sleep(60)

def ingest_and_process_logfiles_from_siem_dir() -> str:
    print("ingested called")
    # network folder access
    siem_logfile_path = f'flask_sse_with_logs/{SIEM_LOGS_DIRECTORY}'
    siem_network_folder_access = SIEMNetworkFolderAccess(
        siem_logfile_access_path=siem_logfile_path
    )
    siem_network_folder_access.parse_and_process_ingested_logfile()
    return INGESTING_STATUS


@siem_route_view_bp.route("/siem_logs", methods=["POST"]) 
def populate_homepage_datatable() -> json:
    log(type=LogLevel.INFO, message="returns records to datatables frontend")

    draw = int(request.form.get("draw", 1))
    row = int(request.form.get("start", 0))  # offset

    # number of records perpage
    rowperpage = int(request.form.get("length", 10))
    search_value = request.form.get("search[value]", "").lower()

    # Total number of records without filtering
    logdata_record_count = db.session.query(SIEMLogsDBtable).count()
    logdata_stmt = select(SIEMLogsDBtable).offset(row).limit(rowperpage)
    logdata_result = db.session.execute(logdata_stmt).scalars().all()

    # Total number of records with filtering
    if search_value != "":
        return queried_search_data(
            search_value=search_value,
            row=row,
            rowperpage=rowperpage,
            draw=draw,
            logdata_record_count=logdata_record_count,
            logdata_result=logdata_result,
        )

    # Convert the result to a list of dictionaries
    processed_logdata = [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "event_type": log.event_type,
            "message": log.message,
            "severity": log.severity,
            "loglevel": log.loglevel,
        }
        for log in logdata_result
    ]

    if len(processed_logdata):
        return jsonify(
            {
                "draw": draw,
                "data": processed_logdata,
                "recordsTotal": logdata_record_count,
                "recordsFiltered": logdata_record_count,
            }
        )

    return default_no_available_data_response()


# non-route-methods
def queried_search_data(
    *,
    search_value: str,
    row: int,
    rowperpage: int,
    draw: int,
    logdata_record_count: int,
    logdata_result: list,
):
    """
    queried_search_data method
        Returns json records of table retrieved from database to be rendered on
        frontend datatable

    search_value:
        Search term typed in search field in frontend-datatable
    row:
        Offset value to start fetching table records from: defaults to 0
    rowperpage:
        Number of records per page returned to frontend-datatables: defaults to 10
    draw:
        Event is fired whenever the table is redrawn on the frontend-page
    logdata_record_count:
        Total number of records without filtering
    logdata_result:
        List of table records to be returned
    """

    db_query_search_result = (
        db.session.query(SIEMLogsDBtable)
        .filter(
            or_(
                SIEMLogsDBtable.id == search_value,
                SIEMLogsDBtable.timestamp.contains(search_value),
                SIEMLogsDBtable.event_type.contains(search_value),
                SIEMLogsDBtable.message.contains(search_value),
                SIEMLogsDBtable.severity.contains(search_value),
                SIEMLogsDBtable.loglevel.contains(search_value),
            )
        )
        .offset(row)
        .limit(rowperpage)
        .all()
    )

    # Convert the result to a list of dictionaries
    processed_logdata = [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "event_type": log.event_type,
            "message": log.message,
            "severity": log.severity,
            "loglevel": log.loglevel,
        }
        for log in db_query_search_result
    ]

    # Convert the result to a list of dictionaries
    if len(processed_logdata):
        return jsonify(
            {
                "draw": draw,
                "data": processed_logdata,
                "recordsTotal": logdata_record_count,
                "recordsFiltered": logdata_record_count,
            }
        )