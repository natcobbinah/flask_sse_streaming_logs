
//https://datatables.net/download/index

$(document).ready(function () {
    // if request needs to be made with CSRF_TOKEN, needs to be uncommented
    // here and the headers attribute as well
    //var csrf_token = $('meta[name=csrf-token]').attr('content')

    //processing logstatus spinner
    var log_ingestion_status_spinner = "#logingestion_status"

    var logrecordsTable = $('#siemlogdatatable').DataTable({
        processing: true,
        serverSide: true,
        searching: true,
        lengthMenu: [[10, 25, 50, 100, 200, 500], [10, 25, 50, 100, 200, 500]],
        pageLength: 10,
        ajax: {
            url: '/siem_logs',
            type: 'POST',
            // headers: {
            //   "X-CSRFToken": csrf_token,
            // },
            success: function(result){
                console.log("Data fetched successfully:", result);
            },
            error: function (error_result) {
                console.log(error_result)
            },
        },
        columns: [
            { 
                data: "id", 
                render: function (data, type, row, meta) {
                    switch(data){
                        case 'not available':
                            //remove all child nodes (button) from div 
                            //becuause on page load button is appended to div 
                            //with datatables making post request, to prevent 
                            //button appended twice
                            $(log_ingestion_status_spinner).empty();

                            //append spinner to div
                            $(log_ingestion_status_spinner).append(
                                `
                                <button class="btn btn-primary" type="button" disabled>
                                    <span class="spinner-border spinner-border-sm"  aria-hidden="true"></span>
                                    <span role="status">Ingesting and processing Logs...Please be patient</span>
                                </button>
                                `
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
    const eventSource = new EventSource("/ingesting_and_processing_siem_logs");

    eventSource.onmessage = function(event) {

        console.log("Event received from server:", event.data);

        //if event is received, trigger data-table to make post request to poulate new data
        if(JSON.parse(event.data).message){
           //logrecordsTable.ajax.reload(null,false);
        }
    };
    
});