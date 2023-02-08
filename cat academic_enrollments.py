from BbApiConnector import BbApiConnector
from bottle import request, response, post, get, put, delete
import json
import csv
import pandas as pd
import datetime

  ############### API Call #####################
api_conn = BbApiConnector('<<<INSERT THE PATH TO YOUR SECRETS JSON FILE HERE')
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
print('API Call Completed')

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
						section_id = each_item["id"]
						ls_sections.append({ "Section_id": section_id})
						count+=1

print('LS iterate  Completed', count)

############### iterate MS #####################
ms_sections = []
count = 0
for key,value in responseOfMSSections.items():
	if isinstance(value, list): # if dictionary contains a list
		for each_item in value: #for each item in list value
				temp = str(v)
				if  len(each_item["teachers"]):
					section_id = each_item["id"]
					ms_sections.append({ "Section_id": section_id})
					count =+1

print('mS iterate  Completed', count)

############### iterate US #####################
us_sections = []
key_list=['name','teachers', 'id' ]
count = 0
for key,value in responseOfUSSections.items():
	if isinstance(value, list): # if dictionary contains a list
		for each_item in value: #for each item in list value
				temp = str(v)
				#print (each_item)
				if  len(each_item["teachers"]):
					section_id = each_item["id"]
				us_sections.append({"Section_id": section_id})
				count =+1

print('US iterate  Completed', count)

#combine sections from each school level
sections = ls_sections + ms_sections + us_sections
print('sections combined  Completed')

#### remove duplicate sections######
result=[]
count = 0
for v in sections: #for each value in the sections list
	for key, value in v.items():
		if value not in result:
			result.append(value)
			count =+1


############ Iterate through list/dictionary of section to create roster ############
#For each section print out roster#
enrollment=[]
count=0
for v in result: #for each value in the list sections
		temp = str(v)
		enrollment_uri = f'https://api.sky.blackbaud.com/school/v1/academics/sections/{temp}/students'
		#print(enrollment_uri)
		req = bb_session.get(enrollment_uri, params=temp)
		responseOfEnrollment = json.loads(req.text)
		count +=1
		#print(count, "This is the enrollment for section:",temp," ",responseOfEnrollment)
		for k,v in responseOfEnrollment.items():
				#print (k,v)
				if not isinstance(v, int):
					for each in v:
						enrollment.append({"Student_id": each["id"], "Section_id": temp, "School_id":'HAHI'})


############### create CSV #####################

enrollments_csv_headers=['Student_id', 'Section_id', 'School_id']

#uses pandas library to write to csv
df = pd.DataFrame(enrollment)
df.to_csv('enrollments.csv', mode='w',index=False, header=enrollments_csv_headers)

print ('csv complete', count)
