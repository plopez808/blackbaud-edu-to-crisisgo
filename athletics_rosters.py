from BbApiConnector import BbApiConnector
from bottle import request, response, post, get, put, delete
import json
import csv
import pandas as pd
import itertools
import sys
 
 
api_conn = BbApiConnector('<<PATH TO SECRETS FILE HERE')
bb_session = api_conn.get_session()

#This will be a dictionary array to traverse each team id
#get teams into list/dictionary
teams_uri = f'https://api.sky.blackbaud.com/school/v1/athletics/teams'
req = bb_session.get(teams_uri)
responseOfTeams = json.loads(req.text)
#responseOfTeams = json.dumps(req, indent=4)
#print(responseOfTeams["value"][0]["id"])
team_ids = []
for key,value in responseOfTeams.items():
	if isinstance(value, list): # if dictionary contains a list
		for each_item in value: #for each item in list value
			#i=1
			for k,v in each_item.items(): # for each dictionary in list
				if k == 'id': #if it is the ID,
					#tempdict.append({k:v})
					team_ids.append(v) 
				else:
					pass
		else:
			pass		
print("these are all the team_ids", team_ids)

############ Iterate through list of teams ############
#For each team print out roster#
for v in team_ids:
	print (v)
	print(type(v))
	temp =str(v)
	token_uri = f'https://api.sky.blackbaud.com/school/v1/athletics/teams/{temp}/roster'
	try:
		req = bb_session.get(token_uri, params=temp)
		print(req)
		response = json.loads(req.text)
		print(response)
	except Exception as e:
		data = {'errors': [str(e)]}
		print(data)

############### create CSV #####################
schools.csv_headers=['School_id','School_name']
teachers.csv_headers=['School_id','Teacher_id','Last_name', 'First_name']
students.csv_headers=['School_id', 'Student_id', 'Last_name', 'First_name']
sections.csv_headers=['School_id', 'Section_id', 'Teacher_id', 'Name', 'Term_start', 'Term_end'
enrollments.csv_headers=['School_id', 'Student_id', 'Section_id']


with open ('staff.csv', 'w', encoding = 'UTF8', newline='') as f:
	#create csv writer oject
	writer = csv.writer(f)
	#write a row to the csv file
	writer.writerow(row)
