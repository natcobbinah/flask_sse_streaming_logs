
//https://datatables.net/download/index

$(document).ready(function () {
    // if request needs to be made with CSRF_TOKEN, needs to be uncommented
    // here and the headers attribute as well
    //var csrf_token = $('meta[name=csrf-token]').attr('content')

    //processing logstatus spinner
    var log_ingestion_status_spinner = "#logingestion_status"

    var logrecordsTable = $('#siemlogtable').DataTable({
        processing: true,
        serverSide: true,
        searching: true,
        lengthMenu: [[10, 25, 50, 100, 200, 500], [10, 25, 50, 100, 200, 500]],
        pageLength: 10,
        ajax: {
            url: '/',
            type: 'POST',
            // headers: {
            //   "X-CSRFToken": csrf_token,
            // },
            error: function (error_result) {
                console.log(error_result)
            },
        },
        columns: [
            { data: 
                "id", 
                render: function(data, type, row, meta){
                    switch(data){
                        case 'not available':
                            $(log_ingestion_status_spinner).empty();

                            $(log_ingestion_status_spinner).append(
                                `button class="btn btn-secondary" type="button" disabled>
                                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                    Ingesting and Processing logs. Please be patient...
                                </button>`
                            );

                            return '<p>not available</p>';

                        default:
                            $(log_ingestion_status_spinner).remove();
                            return data;
                    }
                }
            
            },
            { data: "timestamp" },
            { data: "event_type" },
            { data: "message" },
            { data: "severity" },
            { 
                data: "loglevel",
                render: function (data, type, row, meta) {
                    switch(data){
                        case 'INFO':
                            return `<span class="badge bg-info text-dark">${data}</span>`;  
                        case 'WARN':
                            return `<span class="badge bg-warning text-dark">${data}</span>`;
                        case 'CRITICAL':
                            return `<span class="badge bg-primary text-dark">${data}</span>`;
                        case 'ERROR':
                            return `<span class="badge bg-danger text-dark">${data}</span>`;
                        case 'DEBUG':
                            return `<span class="badge bg-secondary text-dark">${data}</span>`;
                        default:
                            return '<p>not available</p>';
                    }
                }
            },
        ],
    });

    //create  EventSource instance to open a persistent connection to 
    //backend SSE endpoint, which sends events in text/event-stream format
    const eventSource = new EventSource("/ingesting_and_processing_siem_logs")
    
    eventSource.onmessage = function(event){
        console.log("Event received from server:", event.data)
        //if event is received, trigger data-table to make post request to poulate new data
        
        if(JSON.parse(event.data).message){
           logrecordsTable.ajax.reload(null,false);
        }
    };
    
});