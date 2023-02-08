##########
# THIS CODE IS INCOMPLETE AND NOT IN THE CONTROL FILE
#


from BbApiConnector import BbApiConnector
from bottle import request, response, post, get, put, delete
import json
import csv
import pandas as pd
import itertools
import sys
 
  ############### API Call #####################

api_conn = BbApiConnector('<<YOUR APPS SECRET PATH HERE')
bb_session = api_conn.get_session()

#Carter Hall = 4527 ,PF = 4528, Robertston = 4529, Wishard = 4531, PF Summer = 4640
params = {
	'dorm_id': '4527',
	'level_num': '1995'
}
dorm_uri = f'https://api.sky.blackbaud.com/school/v1/dorms/{params["dorm_id"]}/roster?level_num={params["level_num"]}'

req = bb_session.get(dorm_uri, params=params)
CarterResponse = json.loads(req.text)

params = {
	'dorm_id': '4528',
	'level_num': '1995'
}

dorm_uri = f'https://api.sky.blackbaud.com/school/v1/dorms/{params["dorm_id"]}/roster?level_num={params["level_num"]}'

req = bb_session.get(dorm_uri, params=params)
PFResponse = json.loads(req.text)

params = {
	'dorm_id': '4529',
	'level_num': '1995'
}

dorm_uri = f'https://api.sky.blackbaud.com/school/v1/dorms/{params["dorm_id"]}/roster?level_num={params["level_num"]}'

req = bb_session.get(dorm_uri, params=params)
RobertsonResponse = json.loads(req.text)

#except Exception as e:

#	data = {'errors': [str(e)]}
#	print(data)

############### iterate #####################
#interates through nested list to create a new nested list for output to csv
tempList = []
key_list =  ['user_id']
for key,val in sorted(CarterResponse.items()):
	if isinstance(val, list): # if dictionary contains a list
		for each_item in val: #for each item in list value
			#print ('this is each_item', each_item)
				count=0
				for k,v in each_item.items(): # for each dictionary in list
					count+=1
					print(count)
					#if k == 'residents':
					print (v[0][0]["user_id"])							
					#	print ('k1 is:', residents["user_id"])
				#k2 = "Section_id"
			#	k3 = "School_id"
				#tempList.append({k1:temp1, k2: '4529', k3:'HAHI'})

				############### create CSV #####################

#schools_csv_headers=['School_id','School_name']
#teachers_csv_headers=['School_id','Teacher_id', 'First_name', 'Last_name']
#students_csv_headers=['School_id', 'Student_id', 'Last_name', 'First_name']
#sections_csv_headers=['School_id', 'Section_id', 'Teacher_id', 'Name', 'Term_start', 'Term_end'
#enrollments_csv_headers=['School_id', 'Student_id', 'Section_id']

#uses pandas library to write to csv
#df = pd.DataFrame(students_csv_headers)
#df = pd.DataFrame(tempList)
#df.to_csv('enrollment.csv', header =False,index=False)
