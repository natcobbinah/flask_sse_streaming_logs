import os
import random
import json

SIEM_logs_directory ='SIEM_logs'

# generates logs into a specified folder after specific time intervals
def generate_network_server_logs():

    # generated with chatgpt
    random_log_messages = [
        {
            "timestamp": "2025-11-22T10:14:32Z",
            "event_type": "authentication_failure",
            "message": "Failed login attempt detected on VPN gateway. Reason: invalid credentials.",
            "severity": "medium",
            "loglevel": "ERROR"
        },
        {
            "timestamp": "2025-11-22T10:17:09Z",
            "event_type": "malware_detection",
            "message": "Endpoint agent detected Trojan.Generic activity. File quarantined.",
            "severity": "high",
            "loglevel": "CRITICAL"
        },
        {
            "timestamp": "2025-11-22T10:19:51Z",
            "event_type": "file_access",
            "message": "Unusual after-hours file access attempt detected.",
            "severity": "medium",
            "loglevel": "ERROR"
        },
        {
            "timestamp": "2025-11-22T10:23:14Z",
            "event_type": "network_traffic_anomaly",
            "message": "Outbound data transfer exceeds baseline threshold.",
            "severity": "high",
            "loglevel": "CRITICAL"
        },
        {
            "timestamp": "2025-11-22T10:26:58Z",
            "event_type": "privilege_escalation",
            "message": "User account granted sudo privileges unexpectedly.",
            "severity": "critical",
            "loglevel": "CRITICAL"
        },
        {
            "timestamp": "2025-11-22T10:29:41Z",
            "event_type": "ids_alert",
            "message": "IDS detected potential port scanning activity.",
            "severity": "medium",
            "loglevel": "WARN"
        },
        {
            "timestamp": "2025-11-22T10:33:22Z",
            "event_type": "cloud_access",
            "message": "Successful login from new geolocation: Frankfurt, DE.",
            "severity": "low",
            "loglevel": "INFO"
        }
    ]

    filename = f'flask_sse_with_logs/{SIEM_logs_directory}/siem_events.log'
    
    with open(filename, 'a+') as f:
        log_message = random.choice(random_log_messages)
        f.write(f'{json.dumps(log_message)}\n')
