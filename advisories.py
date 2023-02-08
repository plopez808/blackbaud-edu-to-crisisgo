from BbApiConnector import BbApiConnector
from bottle import request, response, post, get, put, delete
import json
 
api_conn = BbApiConnector('<<PATH TO YOUR SECRETS FILE HERE')
bb_session = api_conn.get_session()

params = {
	'level_num': '1995'
}

token_uri = f'https://api.sky.blackbaud.com/school/v1/advisories/sections?level_num={params["level_num"]}'
try:
	req = bb_session.get(token_uri, params=params)
	print(req)
	response = json.loads(req.text)

	print(response)
except Exception as e:

	data = {'errors': [str(e)]}
	print(data)

####################################
