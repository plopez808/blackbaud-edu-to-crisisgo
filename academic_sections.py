from BbApiConnector import BbApiConnector
from bottle import request, response, get
import json
import csv
import pandas as pd
import datetime
 
  ############### API Call #####################
api_conn = BbApiConnector('<<INSERT THE PATH TO YOUR SECRETS FILE HERE')
bb_session = api_conn.get_session()

#US = 1995, MS=1994  , LS=1993, summer=1996

ls_uri = f'https://api.sky.blackbaud.com/school/v1/academics/sections?level_num=1993'
req = bb_session.get(ls_uri)
responseOfLSSections = json.loads(req.text)

ms_uri = f'https://api.sky.blackbaud.com/school/v1/academics/sections?level_num=1994'
req = bb_session.get(ms_uri)
responseOfMSSections = json.loads(req.text)

us_uri = f'https://api.sky.blackbaud.com/school/v1/academics/sections?level_num=1995'
req = bb_session.get(us_uri)
responseOfUSSections = json.loads(req.text)
print('API call done')
############ Get terms API call ###############################################

# API Date format is "2018-08-30T12:00:00Z" converted to MM/DD/YYYY for import
# Academics Offering ID: 1, Activities: 2, Advisory: 3, Dorm: 4, Athletic: 9

terms_uri = f'https://api.sky.blackbaud.com/school/v1/terms'
req = bb_session.get(terms_uri)
responseOfTerms= json.loads(req.text)

#### function to convert times for csv output ####
def convert(date_time):
    format = '%Y-%m-%d' # The format of the in coming string
    date_time = date_time[:10]
    datetime_str = datetime.datetime.strptime(date_time, format) #convert string to date time  formate
    format = '%m/%d/%Y' # The format of the in coming string
    formatted_date = datetime.date.strftime(datetime_str, "%m/%d/%Y") #convert date format to final format for output
    return formatted_date
print('API terms call done')
##################### iterate through terms ###############################

for key,value in responseOfTerms.items():
	if isinstance(value, list): # if dictionary contains a list
		for each_item in value: #for each item in list value
			if each_item["level_id"] == 1993 and each_item["offering_type"] == 1 :	# Gets LS Terms
				LSBeg = convert(each_item["begin_date"])
				LSEnd = convert(each_item["end_date"])

			if each_item[ "level_description"] != 'Entire School':
				if each_item["level_id"] == 1994 and each_item["offering_type"] == 1:
					if each_item["description"] == '1st Semester' :
						MS1Beg = convert(each_item["begin_date"])
						MS1End = convert(each_item["end_date"])
						MS1TermID= each_item["id"]
					elif each_item["description"]  == '2nd Semester':
						MS2Beg = convert(each_item["begin_date"])
						MS2End = convert(each_item["end_date"])
						MS2TermID= each_item["id"]

				if each_item["level_id"] == 1995 and each_item["offering_type"] == 1: # Gets US S1 Academic Terms
					if each_item["description"] =='1st Semester' :
						US1Beg = convert(each_item["begin_date"])
						US1End = convert(each_item["end_date"])
						US1TermID= each_item["id"]
					elif each_item["description"]  == '2nd Semester':
						US2Beg = convert(each_item["begin_date"])
						US2End = convert(each_item["end_date"])
						US2TermID= each_item["id"]
print ("us termID for S1 is:",US1TermID)
print ("us termID for S2 is:",US2TermID)
print('terms done')

############### iterate LS #####################
ls_sections = []
count = 0
for key,value in responseOfLSSections.items():
	if isinstance(value, list): # if dictionary contains a list
		for each_item in value: #for each item in list value
			for k,v in each_item.items(): # for each dictionary in list
				temp = str(v)
				if k == 'name' and count <= 5:
					if 'HOMEROOM' in temp :
						temp1 = each_item["name"]
						teacher_id = each_item["teachers"][0]["id"]
						section_id = str(each_item["id"])
						ls_sections.append({"Name":temp1, "Teacher_id": teacher_id, "Section_id": section_id,"School_id":'HAHI', "Term_start":LSBeg, "Term_end":LSEnd})
						count+=1
print('ls sections done')

############### iterate MS #####################
ms_sections = []
for key,value in responseOfMSSections.items():
	if isinstance(value, list): # if dictionary contains a list
		for each_item in value: #for each item in list value
				#temp = str(v)
				if  len(each_item["teachers"]):
					temp1 = each_item["name"]
					teacher_id = each_item["teachers"][0]["id"]
					section_id = each_item["id"]
					term_id = str(each_item["duration"]["id"])
					if term_id == str(MS1TermID):
						ms_sections.append({"Name":temp1, "Teacher_id": teacher_id, "Section_id": section_id, "School_id":'HAHI', "Term_start":MS1Beg, "Term_end":MS1End})
					elif term_id == str(MS2TermID):
						ms_sections.append({"Name":temp1, "Teacher_id": teacher_id, "Section_id": section_id, "School_id":'HAHI', "Term_start":MS2Beg, "Term_end":MS2End})
print('ms sections done')

############### iterate US #####################
us_sections = []
count= 0
for key,value in responseOfUSSections.items():
	if isinstance(value, list): # if dictionary contains a list
		for each_item in value: #for each item in list value
				#temp = str(v)
				if len(each_item["teachers"]):
					count+=1
					temp1 = each_item["name"]
					teacher_id = each_item["teachers"][0]["id"]
					section_id = each_item["id"]
					term_id = str(each_item["duration"]["id"])
					if term_id == str(US1TermID):
						us_sections.append({"Name":temp1, "Teacher_id": teacher_id, "Section_id": section_id, "School_id":'HAHI', "Term_start":US1Beg, "Term_end":US1End})
					elif term_id == str(US2TermID):
						us_sections.append({"Name":temp1, "Teacher_id": teacher_id, "Section_id": section_id, "School_id":'HAHI', "Term_start":US2Beg, "Term_end":US2End})
print('us sections done')

############### create CSV #####################
#
sections_csv_headers = ['Name','Teacher_id', 'Section_id','School_id', 'Term_start', 'Term_end']

#uses pandas library to write to csv
df = pd.DataFrame(ls_sections)
df.to_csv('sections.csv', mode='w',index=False, header=sections_csv_headers)
print('LS sections added successfully')

df = pd.DataFrame(ms_sections)
df.drop_duplicates(subset=['Section_id'], keep='first', inplace=True)
df.to_csv('sections.csv', mode='a',index=False, header=None)
print('MS sections added successfully')

df = pd.DataFrame(us_sections)
df.drop_duplicates(subset=['Section_id'], keep='first', inplace=True)
df.to_csv('sections.csv', mode='a',index=False, header=None)
print('US sections added successfully')
print ('csv complete')
