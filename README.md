# Blackbaud Education Management APIs to FTP CrisisGo 
You will need BbApiConnector-Python found here in Github. 
Go will need access to Blackbaud K-12 Developer Sky API subscription. 
You will need to create an Blackbaud App for the API to run.
In the BbApi Connector resources => app_secrets JSON file add the app id from the app you created, app secret, tokens you get from the setup up the BbApi Connector, subscription key from the app you created, and the URI which is localhost:port/callback. 
You will need to intall the panda, requests, pysftp, jsonify BbApiConnector-justein python library. 

Add clever_control.sh to cronjobs to run nightly or however often you choose. 
The script crisis_control.sh runs the following python scripts via a nightly cronjob.

studentsAPI.py #grabs all students. Creates students.csv
staffAPI.py #grabs all dorm leaders, teachers, activity leaders, coaches and advisors and creates teachers.csv
schools_csv.py #creates generic schools file. school_id can be anything we choose 
but has to match in the other files. Creates schools.csv
academic_sections.py #creates academic sections with teachers and creates sections.csv
academic_enrollment.py #creates enrollment rosters for each sections and creates enrollments.csv
dorm_enrollment.py # incomplete but will be used to import dorm groups
advisory_enrollment.py #incomplete but will used to import advisory groups.

to produce the following
schools.csv #per crisisgo Documentation bldg name must match school name
students.csv #no duplicate student ids
teachers.csv #no duplicate teacher ids 
sections.csv #no duplicate section ids teachers must exist in previous csv
enrollments.csv #student ids and section ids must exist in previous csv

and then runs
sftp.py 
to send all 5 csvs via sftp to crisisGo. 
There is a nightly autosyn in crisisGo dashboard. 
This can also be manually compelted for testing.
