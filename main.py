#!/usr/bin/env python

from flask import Flask, render_template, request, g
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

@app.route('/', methods=['GET', 'POST'])
def index():
	return "The api can be found at /api"

@app.route('/api', methods=['GET', 'POST'])
def api():

	try:
		startTimestamp = request.args['startTimestamp']
		endTimestamp = request.args['endTimestamp']
	except:
		return "No or incomplete form data received"

	# Attempt to Query DB
	try:
		#results = query_db("SELECT * FROM calendar WHERE datetime(start, 'unixepoch') >= datetime(%s, 'unixepoch') AND datetime(end, 'unixepoch') <= datetime(%s, 'unixepoch') ORDER BY datetime(start, 'unixepoch') ASC;" %(startTimestamp, endTimestamp))
		results = query_db("SELECT * FROM calendar;")
	except: #error as e:
		raise
		#return "Error: %s" %(e.value)

	return "Start Time: %s<br>End Time: %s<br> %s" %(startTimestamp, endTimestamp, results)

	

if __name__ == '__main__':
	app.run(debug = True)