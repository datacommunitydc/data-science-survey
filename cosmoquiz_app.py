# all the imports
#from __future__ import with_statement
#from contextlib import closing
from flask import Flask, request, session, make_response, g, redirect, url_for, abort, render_template, flash

import random
import os
import csv
import re

import blurbs
import results as r

import config
from models import *

from datetime import datetime



# configuration
#DATABASE = '/tmp/badges.db'
#USERNAME = 'admin'
#PASSWORD = 'default'
#SERVER_NAME = 'http://www.dancesportlife.com/cosmoquiz/'
#ROOT_PATH = '/home5/dancespo/public_html/cosmoquiz/'
#DEBUG = True
#SECRET_KEY = '\xb7Fr\xbd7TQ\x7f9]\xafr\xf0\xa9\xe70Q\xbcY\xe8\xe8\x00v\xa6'
#CSRF_ENABLED = True


# create application
app = Flask(__name__.split('.')[0])
app.config.from_object(__name__)
#app.config.from_object('config.DevelopmentConfig')
app.config.from_object('config.ProductionConfig')

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/badges.db'



@app.route('/index')
@app.route('/')
def start():
	if ( ('results_computed' in session) and (session['results_computed']) ):
		return (render_template('results.html', 
			blurb = blurbs.pick_blurb(session['skill_score_ndx_max'],session['self_id_score_ndx_max']), 
			skill=session['skill_label'], 
			selflabel=session['self_label']
		))
	else:
		session['user_id'] = str(random.randint(1, 999999))

		if app.config['DEBUG']:
			print(session['user_id'])
	
		return (render_template('index.html'))
	
@app.route('/q1')
def q1():
	if app.config['DEBUG']:
		print(session['user_id'])
	return (render_template('question1.html'))
	
@app.route('/q2', methods=['post'])
def q2():
	data = request.form
	q1 =  data.getlist('id_name',type=float)
	session['q1']= q1
	return (render_template('question2.html'))	

@app.route('/surveydetails')
def surveydetails():
	return (render_template('surveydetails.html'))

@app.route('/faq')
def faq():
	return (render_template('faq.html'))

@app.route('/results', methods=['post'])
def results():
	session['q2'] = [ float(request.form['scientist']), 
					float(request.form['engineer']),
					float(request.form['bp']), 
					float(request.form['artist']),
					float(request.form['researcher']),
					float(request.form['stats']),
					float(request.form['jack']),
					float(request.form['leader']),
					float(request.form['ent']),
					float(request.form['dev']),
					float(request.form['ds']) ]					

	#Inserting database write instead of dump to file
	result = Result(str(session['q1']).strip('[]'), str(session['q2']).strip('[]'), session['user_id'],datetime.utcnow(),str(request.remote_addr))
	
	#UPDATE THIS!
	db.session.add(result)
	db.session.commit()

	#write results to file with session id
	""""
	fname = "results/" + str(session['user_id']) + ".txt"
	try: 
		f = open(fname,"w'")
		wr = csv.writer(f)		
		wr.writerow([session['user_id'], session['q1'], session['q2'] ])
		f.close()
	except IOError as e:
		print "File write error"
	"""
						
	#need to compute results to display, everything stored in session
	r.compute_results(session, app.config['DEBUG'])

	session['results_computed'] = True
	#need to return a block of text to 

	print request.remote_addr
	print datetime.utcnow()

	if app.config['DEBUG']:
		print "++++++++"
		print session['skill_label']
		print session['self_label']
		print session.keys(), '\n'

	skill_colors = ["orange", "green", "blue", "purple", "red"]
	self_id_colors = ["#fdc592", "#b8f997", "#fba2c3", "#b3effe"]

	return (render_template('results.html', 
				blurb = blurbs.pick_blurb(session['skill_score_ndx_max'],session['self_id_score_ndx_max']), 
				skill=session['skill_label'],
				skill_color = skill_colors[session['skill_score_ndx_max']], 
				selflabel=session['self_label'],
				self_id_color = self_id_colors[session['self_id_score_ndx_max']]
			))

@app.route('/reset')
def reset():
	for key in session.keys():
		del(session[key])

	session['results_computed'] = False

	if app.config['DEBUG']:
		print session.keys()
	
	return (start())


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
