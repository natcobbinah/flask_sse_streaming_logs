# BUILD REAL-TIME LOG-EVENTS DASHBOARD USING FLASK and SERVER-SENT-EVENTS
This application demonstrates  the ingestion of telemetric data; for this purpose, logs. are written to a centralized SIEM system, where they 
are parsed and processed with results showcased on dashboards so IT, or  the development team, can easily see how the application is responding as it is 
being used by users both externally and internally, so that real-time fixes can be carried out to curb incidents that occur in the long term.

## STEPS TO RUN THE APPLICATION LOCALLY
1. Clone the application from this repository
2. Change directory (cd) to **flask_sse_with_logs** using your IDE or terminal program of choice
3. Create a python virtual environment (so as not to pollute your existing environment) with packages that will be installed  to ensure the working of this application
4. Activate the virtual environment
   ```
    on Windows: 
   .venv/Scripts/activate

   on mac/linux
   .venv/bin/activate
   ```
6. Install the packages listed in the **requirements.txt** file
   ```
   pip install -r requirements.txt
   ```

8. Run the application by typing, **flask run** on the **IDEs** or **CLI** to launch the application
9. Visit the url_path, usually (127.0.0.1:5000) on the terminal, to access the Real-Time LogEvent dashboard

## SAMPLE IMAGES SHOWING THE WORKING APPLICATION AND THE VARIOUS STATES BEFORE THE LOG-EVENTS DASHBOARD IS VIEWED BY END-USERS
 ### Backend Application Start
<img width="1920" height="1080" alt="application start backend" src="https://github.com/user-attachments/assets/f86f3b35-ed90-478a-8d72-fd597007794e" />

 ### Frontend Application Start
<img width="1366" height="768" alt="application start" src="https://github.com/user-attachments/assets/3d6de1d9-5fe0-4ae1-b7b5-b16b66feb3ab" />

 ### Logfile content on Application Start
<img width="1920" height="1080" alt="siem_logfile_on_application_startup" src="https://github.com/user-attachments/assets/6ade998b-f82d-4e10-b71c-ee86d8de4f8e" />

 ### LogDatabase table on Application Start (Using SQLITE as database storage for illustrative purposes)
<img width="1366" height="768" alt="siemlogs_dbtable_before_application_start" src="https://github.com/user-attachments/assets/50ab8183-d6ef-4298-ac4d-0e583374d3b4" />

 ### LogDatabase Ingested Logfile properties on Application Start
<img width="1366" height="768" alt="siem_logfile_properties_before_application_starts" src="https://github.com/user-attachments/assets/531f6373-3ace-4243-a035-6a7163c9c158" />

 ### Logfile content after application starts and content added to it the first time
<img width="1920" height="1080" alt="siem logfile written to the first time" src="https://github.com/user-attachments/assets/9eba168a-d8d4-4e65-94a9-89f9e4800545" />

 ### LogDatabase table after application starts and records added to it the first time
<img width="1369" height="374" alt="db written to the first time" src="https://github.com/user-attachments/assets/5db82c11-a2d5-4383-a599-bc4e2ab477d1" />

 ### LogDatabase Ingested Logfile properties after application starts and records added to it the first time
<img width="1385" height="259" alt="db file properties written to the first time" src="https://github.com/user-attachments/assets/187fa451-b33d-45ec-beff-abad86245ee8" />

 ### Logfile content after application runs for sometime
<img width="1920" height="1080" alt="siem_logfile after application runs for sometime" src="https://github.com/user-attachments/assets/00491ce3-6c29-436f-9efc-ece168d34788" />

 ### LogDatabase table after  application runs for sometime
<img width="1366" height="768" alt="db after application runs for sometime" src="https://github.com/user-attachments/assets/94e63d69-e3ae-4f23-b949-6100c4ede7c5" />

 ### LogDatabase Ingested Logfile properties after application runs for sometime
<img width="1381" height="304" alt="db size after application runs for sometime" src="https://github.com/user-attachments/assets/dfe1cef0-c5b4-482b-8956-699d08286ceb" />

 ### Frontend after application runs for sometime
<img width="1366" height="768" alt="homepage datatable after logingestion runs for sometime" src="https://github.com/user-attachments/assets/91cd69fa-248e-4bef-906b-172ac7f72017" />



