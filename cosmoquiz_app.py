# all the imports
#from __future__ import with_statement
#from contextlib import closing

from flask import Flask, request, session, make_response, g, redirect, url_for, abort, render_template, flash


#import sqlite3
import random
import os
import csv
import re

import blurbs
import results as r
from models import *



# configuration
DATABASE = '/tmp/badges.db'
USERNAME = 'admin'
PASSWORD = 'default'
#SERVER_NAME = 'http://www.dancesportlife.com/cosmoquiz/'
#ROOT_PATH = '/home5/dancespo/public_html/cosmoquiz/'
DEBUG = True
SECRET_KEY = '\xb7Fr\xbd7TQ\x7f9]\xafr\xf0\xa9\xe70Q\xbcY\xe8\xe8\x00v\xa6'
CSRF_ENABLED = True


# create application
app = Flask(__name__.split('.')[0])
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

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
		print(session['user_id'])
		return (render_template('index.html'))
	
@app.route('/q1')
def q1():
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

	#print session['q1']
	#print str(session['q2']).strip('[]')

	#Inserting database write 
	result = Result(str(session['q1']).strip('[]'), str(session['q2']).strip('[]'), session['user_id'])
	#result = Result('bob','sean',session['user_id'])
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
	r.compute_results(session)

	session['results_computed'] = True
	#need to return a block of text to 
	print "++++++++"
	print session['skill_label']
	print session['self_label']
	print session.keys(), '\n'
	#your_blurb = blurbs.pick_blurb(session['skill_score_ndx_max'],session['self_id_score_ndx_max'])


	#your_blurb = "As a Data Businessperson with Math, Algorithms or Operations Research talents, you may be coming at Data Science from a different perspective than a lot of your peers -- you probably haven't embraced the new buzzwords. But you've as committed as anyone to the value of rigorous analysis around organizational data, and to the importance of making optimal use of that data. You're more likely to be female than many other types of Data Scientists, although it's definitely a male-dominated community. Focus on your strengths -- problem solving, thinking outside the box, working in teams to get amazing results. But it's worth keeping current in other areas -- consider learning more about Big Data technology, or picking up some new statistical techniques."
	return (render_template('results.html', 
				blurb = blurbs.pick_blurb(session['skill_score_ndx_max'],session['self_id_score_ndx_max']), 
				skill=session['skill_label'], 
				selflabel=session['self_label']
			))

@app.route('/reset')
def reset():
	for key in session.keys():
		del(session[key])

	session['results_computed'] = False
	print session.keys()
	return (start())


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


"""
##Database functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)   


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


    	<!--I could generate programmatically the list used in q1 by placing this code in the template
	{% for i , s in skills %}
           <li id = "rank_{{i}}" class="ui-state-default"><em>{{ s }}</em> </li>
   {% endfor %}
-->
"""