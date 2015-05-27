from flask import Flask, render_template,redirect,
import json
import os

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

@app.route('/create-db')
def createdb():
	con = mysql.connect()
	with app.open_resource('create-db.sql', mode='r') as f:
		con.cursor().execute(f.read())
	con.commit()
	return
