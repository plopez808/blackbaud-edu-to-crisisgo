# blackbaud-edu-to-crisisgo
The script crisis_control.sh runs the following python scripts via a nightly cronjob.

studentsAPI.py #grabs all students
staffAPI.py #grabs all dorm leaders, teachers, activity leaders, coaches and advisors
schools_csv.py #creates generic schools file. school_id can be anything we choose 
but has to match in the other files
academic_sections.py #creates academic sections with teachers
academic_enrollment.py #creates enrollment rosters for each sections
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
