#!/usr/bin/env python

from flask import Flask, render_template, request, g, json
import sqlite3

app = Flask(__name__)

DATABASE = './calendar.sql'

def connect_to_database():
	try:
		return sqlite3.connect(DATABASE)
	except:
		raise #UnableToConnect("Unable to connect to the Database") 

def query_db(query, args=(), one=False):
	try:
		cur = get_db().execute(query, args)
		rv = cur.fetchall()
		cur.close()
		return (rv[0] if rv else None) if one else rv
	except:
		raise #UnableToQuery("Unable to query the Database")

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		try:
			db = g._database = connect_to_database()
		except:
			raise #UnableToConnect("Unable to connect to the Database") 
	return db

def commit_db():
	print("running db commit")
	db = getattr(g, '_database', None)
	if db is not None:
		db.commit()

def db_to_json(dbresponse):
	'''
	Takes a list of truples from the dbresponse and returns json list
	'''

	listdict = []
	for result in dbresponse:
		listdict.append(
			{
				"id" : result[0],
				"title" : result[1],
				"description" : result[2],
				"location" : result[3],
				"name" : result[4],
				"url" : result[5],
				"start" : result[6],
				"end" : result[7],
			}
		)
	return json.dumps(listdict)

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("calendar.html")

@app.route('/api', methods=['GET', 'POST'])
def api():

	try:
		startTimestamp = request.args['start']
		endTimestamp = request.args['end']
	except:
		pass
		#return "No or incomplete form data received"

	# Attempt to Query DB
	try:
		#results = query_db("SELECT * FROM calendar WHERE datetime(start) >= datetime(%s) AND datetime(end) <= datetime(%s) ORDER BY datetime(start) ASC;" %(startTimestamp, endTimestamp))
		results = query_db("SELECT * FROM calendar WHERE datetime(start) >= datetime(%s, 'unixepoch') AND datetime(end) <= datetime(%s, 'unixepoch') ORDER BY datetime(start) ASC;" %(startTimestamp, endTimestamp))
	except:
		raise


	'''''
	testresult = '''
	[
		{
			"id" : "1",
			"title" : "Test Event 1",
			"description" : "This is the first test event",
			"start" : "2014-05-06 05:30:26",
			"end" : "2014-05-07 05:30:26",
			"location" : "Acme Hall, Room 101",
			"name" : "John Smith"
		}
	]
	'''
	'''''

	#return testresult

	return(db_to_json(results))

	#return jsonify({'results':results})


if __name__ == '__main__':
	app.run(debug = True)