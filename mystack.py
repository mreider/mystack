from flask import Flask, render_template,redirect,request,session
import uuid
import os
import urllib2,urllib,requests
import json
import logging
from logging.handlers import RotatingFileHandler
import pytz
from datetime import datetime
from flaskext.mysql import MySQL
from collections import OrderedDict

mytz = pytz.timezone('America/Los_Angeles')
port = int(os.getenv("PORT"))
vcap = json.loads(os.environ['VCAP_SERVICES'])
svc = vcap['cleardb'][0]['credentials']
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://mystack.xyz/auth'
client_access_token = ''

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'
app.config['MYSQL_DATABASE_USER'] = svc['username']
app.config['MYSQL_DATABASE_PASSWORD'] = svc['password']
app.config['MYSQL_DATABASE_DB'] = svc['name']
app.config['MYSQL_DATABASE_HOST'] = svc['hostname']

mysql = MySQL()
mysql.init_app(app)

class Task:
	pass

@app.route('/create-db')
def createdb():
	con = mysql.connect()
	with app.open_resource('dump3.sql', mode='r') as f:
		con.cursor().execute(f.read())
	con.commit()
	return

@app.route('/')
def index():
    """
    Main entry point
    """
    return render_template('index.html')

@app.route('/login')
def login():
	random_state = uuid.uuid4()
	url = 'https://www.wunderlist.com/oauth/authorize?client_id='+CLIENT_ID+'&redirect_uri='+redirect_uri+'&state='+str(random_state)
	return redirect(url, code=302)

@app.route('/auth')
def auth():
	code = request.args.get('code')
	print code
	request_data = {"client_id":CLIENT_ID,"client_secret":CLIENT_SECRET,"code":code}

	url = 'https://www.wunderlist.com/oauth/access_token'
	httprequest = urllib2.Request(url,request_data,headers={"Content-Type": "application/json"})
	response = requests.post(url,data=request_data)
	data = json.loads(response.content)
	client_access_token = data['access_token']
	session['token'] = client_access_token
	return redirect('/home')

@app.route('/home')
def home():
	open_tasks = []
	closed_tasks = []
	task_positions = OrderedDict()
	tasks = []
	print 'token' not in session
	if 'token' not in session :
		print 'token not in session'
		username = request.args.get('username')
		if username :
			print 'Username %s'%username
			acces_token = get_token(username.lower().replace(' ','.'))
			print 'token %s'%acces_token
			if acces_token:
				session['token'] = acces_token
	print session['token']
	#Get User details
	user_url = 'https://a.wunderlist.com/api/v1/user'
	response = requests.get(user_url,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
	user_data = json.loads(response.content)

	username = user_data['name']
	username = username.lower().replace(' ','.')

	forced = request.args.get('forced')
	need_refresh = need_to_refresh()
	if not need_refresh and not forced:
		data = fetch_user(username,'open')
		print data
		for item in data :
			date_str = item['started'].strftime("%B %d, %Y %I:%M %p") if item['started'] else ''
			tasks.append((item['task_id'],item['task_name'],date_str,item['since'],item['position']))
		return render_template('home.html',lists=tasks,operation='ongoing',user=username)


	url = 'https://a.wunderlist.com/api/v1/lists'
	print 'ACessToken %s'%session['token']

	#Get list details for MyStack list
	response = requests.get(url,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
	#httprequest = urllib2.Request(url,headers={"Content-Type": "application/json","X-Access-Token":client_access_token,"X-Client-ID":CLIENT_ID})
	#response = urllib2.urlopen(httprequest)
	data = json.loads(response.content)
	app.logger.info('Data %s'%data)
	for item in data :
		if item['title'] == 'My Stack':
			list_id = item['id']
	index = 0
	save_access_token(username,session['token'])
	closed_task_ids = []
	#If such list is present fetch reamning details.
	if list_id :
		app.logger.info('List ID %s'%list_id)
		requestdata = {'list_id':list_id}

		#Fetch open tasks
		url = 'https://a.wunderlist.com/api/v1/tasks'
		response = requests.get(url,params=requestdata,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
		data = json.loads(response.content)

		app.logger.info('Open Tasks - Data %s'%data)
		for task in data :
			open_tasks.append((task['id'],task['title']))
		#Fetch completed tasks
		requestdata.__setitem__('completed',True)
		response = requests.get(url,params=requestdata,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
		data = json.loads(response.content)
		for task in data :
			closed_tasks.append((task['id'],task['title']))
			closed_task_ids.append(task['id'])
		#Fetch order
		url = 'https://a.wunderlist.com/api/v1/task_positions'
		response = requests.get(url,params=requestdata,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
		data = json.loads(response.content)
		app.logger.info('Positions  - Data %s'%data)
		for task in data[0]['values']:
			if task not in closed_task_ids:
				task_positions.__setitem__(task,index)
				index+=1

		app.logger.info('Closed Tasks - Data %s'%data)
		#Update db with latest data
		update_db(username,open_tasks,closed_tasks,task_positions)
		#Fetch data from DB for all open tasks
		data = fetch_user(username,'open')
		print data
		for item in data :
			date_str = item['started'].strftime("%B %d, %Y %I:%M %p") if item['started'] else ''
			tasks.append((item['task_id'],item['task_name'],date_str,item['since'],item['position']))
		return render_template('home.html',lists=tasks,operation='ongoing',user=username)

	else :
		lists = []

	return render_template('home.html',lists=tasks,operation='ongoing',user=username)

@app.route('/public')
def public_refresh():
	open_tasks = []
	closed_tasks = []
	task_positions = OrderedDict()
	tasks = []
	print 'token' not in session
	if 'token' not in session :
		print 'token not in session'
		username = request.args.get('user')
		if username :
			print 'Username %s'%username
			acces_token = get_token(username.lower().replace(' ','.'))
			print 'token %s'%acces_token
			if acces_token:
				session['token'] = acces_token
	print session['token']
	#Get User details
	user_url = 'https://a.wunderlist.com/api/v1/user'
	response = requests.get(user_url,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
	user_data = json.loads(response.content)

	username = user_data['name']
	username = username.lower().replace(' ','.')

	forced = request.args.get('forced')
	need_refresh = need_to_refresh()


	url = 'https://a.wunderlist.com/api/v1/lists'
	print 'ACessToken %s'%session['token']

	#Get list details for MyStack list
	response = requests.get(url,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
	#httprequest = urllib2.Request(url,headers={"Content-Type": "application/json","X-Access-Token":client_access_token,"X-Client-ID":CLIENT_ID})
	#response = urllib2.urlopen(httprequest)
	data = json.loads(response.content)
	app.logger.info('Data %s'%data)
	for item in data :
		if item['title'] == 'My Stack':
			list_id = item['id']
	index = 0
	save_access_token(username,session['token'])
	closed_task_ids = []
	#If such list is present fetch reamning details.
	if list_id :
		app.logger.info('List ID %s'%list_id)
		requestdata = {'list_id':list_id}

		#Fetch open tasks
		url = 'https://a.wunderlist.com/api/v1/tasks'
		response = requests.get(url,params=requestdata,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
		data = json.loads(response.content)

		app.logger.info('Open Tasks - Data %s'%data)
		for task in data :
			open_tasks.append((task['id'],task['title']))
		#Fetch completed tasks
		requestdata.__setitem__('completed',True)
		response = requests.get(url,params=requestdata,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
		data = json.loads(response.content)
		for task in data :
			closed_tasks.append((task['id'],task['title']))
			closed_task_ids.append(task['id'])
		#Fetch order
		url = 'https://a.wunderlist.com/api/v1/task_positions'
		response = requests.get(url,params=requestdata,headers={"Content-Type": "application/json","X-Access-Token":session['token'],"X-Client-ID":CLIENT_ID})
		data = json.loads(response.content)
		app.logger.info('Positions  - Data %s'%data)
		for task in data[0]['values']:
			if task not in closed_task_ids:
				task_positions.__setitem__(task,index)
				index+=1

		app.logger.info('Closed Tasks - Data %s'%data)
		#Update db with latest data
		update_db(username,open_tasks,closed_tasks,task_positions)
		#Fetch data from DB for all open tasks
		data = fetch_user(username,'open')
		print data
		for item in data :
			date_str = item['started'].strftime("%B %d, %Y %I:%M %p") if item['started'] else ''
			tasks.append((item['task_id'],item['task_name'],date_str,item['since'],item['position']))
		return json.dumps({"lists":tasks,"operation":'ongoing',"user":username});

	else :
		lists = []

	return json.dumps({"lists":tasks,"operation":'ongoing',"user":username})

@app.route('/u/<username>')
def get_user_list(username):
	tasks = []
	username = username.lower().replace(' ','.')
	data = fetch_user(username,'open')
	print data
	for item in data :
		date_str = item['started'].strftime("%B %d, %Y %I:%M %p") if item['started'] else ''
		tasks.append((item['task_id'],item['task_name'],date_str,item['since'],item['position']))
	return render_template('home.html',lists=tasks,operation='ongoing',user=username)

@app.route('/u/<username>/history')
def get_user_history(username):
	tasks = []
	username = username.lower().replace(' ','.')
	data = fetch_user(username,'closed')
	print data
	for item in data :
		date_str = str(item['started'])
		tasks.append((item['task_id'],item['task_name'],date_str,item['since'],item['position']))
	return render_template('home.html',lists=tasks,operation="history",user=username)

def update_db(username,open_tasks,closed_tasks,task_positions):
	#try:
		#con = mysql.connect()
		#cursor =  con.cursor()

		#Fetch all tasks and positions
		taskmap = fetch_all_usertasks(username)

		app.logger.info('Open Tasks %s'%open_tasks)
		app.logger.info('Task Positions %s'%task_positions)
		open_task_ids = []
		closed_task_ids = []

		for item in open_tasks:
			task_id = item[0]
			open_task_ids.append(task_id)
			position = task_positions.get(task_id) if task_id in task_positions else len(open_tasks)+1
			status = 'started' if position == 0 else 'open'
			old_status = taskmap.get(task_id).status if task_id in taskmap else ''
		 	#print 'Started Time %s for Task %s'%(taskmap.get(task_id).started,task_id)
			if task_id in taskmap:
				#Calculate all the updates
				print 'Old Status %s and status %s'%(old_status,status)
				if old_status == 'started' and status == 'started':
					update_user_task(username,task_id,item[1],status,position,taskmap.get(task_id).started)
				else :
					update_user_task(username,task_id,item[1],status,position)
			else :
				#Calculate all inserts
				create_new_usertask(username,task_id,item[1],status,position)

		#app.logger.info('Closed Tasks %s'%closed_tasks)
		for item in closed_tasks:
			task_id = item[0]
			closed_task_ids.append(task_id)
			#app.logger.info('Adding closed Task %s'%task_id)
			position = task_positions.get(task_id) if task_id in task_positions else len(open_tasks)+1
			if task_id in taskmap:
				#Calculate all the updates
				update_user_task(username,task_id,item[1],'closed',position)
			else :
				#Calculate all inserts
				#app.logger.info('Adding closed Task ')
				create_new_usertask(username,task_id,item[1],'closed',position)
		for task_id in taskmap:
			if task_id not in open_task_ids and task_id not in closed_task_ids:
				#We can assume that the task is deleted .So we can delete it from our tables as well.
				delete_user_task(username,task_id)
		#con.commit()
	# finally:
		#cursor.close()
		#con.close()

def save_access_token(username,access_token):
	try:
		con = mysql.connect()
		cursor =  con.cursor()
		query = 'replace into user_tokens set user= %s , access_token=%s , refreshedat = %s;'
		cursor.execute(query,[username,access_token,datetime.now(mytz)])
		con.commit()
	finally:
		cursor.close()
		con.close()


def create_new_usertask(username,task_id,task_name,status,position):
	try:
		con = mysql.connect()
		cursor =  con.cursor()
		app.logger.info('Inserting taksk %s'%task_id)
		status = 'started' if position == 0 and status == 'open' else status
		started = datetime.now(mytz) if status == 'started' else None
		app.logger.info('Status -->%s'%status)
		query = 'insert into user_tasks (task_id,user,task_name,status,position,started) values(%s,%s,%s,%s,%s,%s)'
		cursor.execute(query,[task_id,username,task_name,status,position,started])

		con.commit()
	finally:
		cursor.close()
		con.close()

def update_user_task(username,task_id,task_name,status,position,started_time=None):
	try:
		con = mysql.connect()
		cursor =  con.cursor()
		#app.logger.info('Updating taksk %s,%s'%(task_id,status))
		query = 'update user_tasks set status = %s , position = %s , started = %s where task_id = %s '
		status = 'started' if position == 0 else status
		if started_time:
			#print 'Already started Task %s '%task_id
			started = started_time
		else:
			#print 'Starting now%s '%task_id
			started = datetime.now(mytz) if status == 'started' else None
		cursor.execute(query,[status,position,started,task_id])

		con.commit()
	finally:
		cursor.close()
		con.close()

def delete_user_task(username,task_id):
	try:
		con = mysql.connect()
		cursor =  con.cursor()
		app.logger.info('Going to delete task %s'%task_id)
		query = 'delete from user_tasks where task_id = %s '
		cursor.execute(query,[task_id])

		con.commit()
	finally:
		cursor.close()
		con.close()

def fetch_user(username,status):
	try:
		con = mysql.connect()
		cursor = con.cursor()
		if status == 'closed':
			query = 'select task_id,user,task_name,started,completed,position from user_tasks where user = %s and status = %s'
		elif len(status) > 0:
			status = 'closed'
			query = 'select task_id,user,task_name,started,completed,position from user_tasks where user = %s and status != %s'
		print query
		print username
		print status
		cursor.execute(query,[username,status])
		data = []
		for task_id,user,task_name,started,completed,position in cursor:
			since = 0
			if completed and started:
				since  = completed - started
				since = since.days
			data.append({'task_id':task_id,'user':user,'task_name':task_name,'started':started,'since':since,'position':position})
		data.sort(key=lambda item:item['position'])
		return data
	finally:
		cursor.close()
		con.close()
def fetch_all_usertasks(username):
	try:
		con = mysql.connect()
		cursor = con.cursor()
		query = 'select task_id,user,task_name,status,position,started from user_tasks where user = %s'

		cursor.execute(query,[username])
		data = {}
		for task_id,user,task_name,status,position,started in cursor:
			task = Task()
			task.task_id = task_id
			task.user = user
			task.task_name = task_name
			task.status = status
			task.position = position
			task.started = started
			data.__setitem__(task_id,task)
		return data
	finally:
		cursor.close()
		con.close()

def need_to_refresh():
	try:
		con = mysql.connect()
		cursor = con.cursor()
		query = 'select refreshedat from user_tokens where access_token = %s'

		cursor.execute(query,[session['token']])
		data = {}
		for refreshedat in cursor:
			current_time = datetime.now(mytz)
			if refreshedat:
				delta = current_time - refreshedat[0]
				return delta.seconds >= 30*60
		return True
	finally:
		cursor.close()
		con.close()


def get_token(username):
	try:
		con = mysql.connect()
		cursor = con.cursor()
		query = 'select access_token from user_tokens where user = %s'
		print 'User name in Fetch %s'%username
		cursor.execute(query,[username])
		for access_token in cursor:
			print 'AcessToken %s'%access_token[0]
			return access_token[0]
	finally:
		cursor.close()
		con.close()

if __name__ == "__main__":
    #handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=10)
    #handler.setLevel(logging.INFO)
    #app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=port, debug=True)
