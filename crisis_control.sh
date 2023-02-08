#!/bin/bash
#
# CRISISGO_CONTROL.SH - run as a crontab job to create and sftp atrium data files to atrium
#
# 10/28/21 PGL
#
cd <<THE PATH TO THIS SCRIPT AND PTYHON FILES>>#go to absolute path of script
python3 studentsAPI.py  #create the students.csv
python3 staffAPI.py #create the teachers.csv to include all dorm parents, coaches etc
python3 school_csv.py #create one column made up school id to match with others csv
python3 academic_sections.py #create sections.csv
python3 academic_enrollments.py #create  enrollments.csv
python3 sftp.py #send data
