from flask import jsonify

def default_no_available_data_response():
    """
    default_no_available_data_response
        returns default json record to frontend-datable when no logfile record has been uploaded to be 
        processed and rendered 
    """
    NO_AVAILABLE_DATA = "not available"
    
    return jsonify(
        {
            "id": NO_AVAILABLE_DATA,
            "timestamp": NO_AVAILABLE_DATA,
            "event_type": NO_AVAILABLE_DATA,
            "message": NO_AVAILABLE_DATA,
            "severity": NO_AVAILABLE_DATA,
            "loglevel": NO_AVAILABLE_DATA,
        }
    )