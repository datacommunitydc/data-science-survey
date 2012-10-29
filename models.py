from flask_sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy

from cosmoquiz_app import app

db = SQLAlchemy(app)

class Result(db.Model):
	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True)
	session_id = db.Column(db.Integer)
	q1 = db.Column(db.String)
	q2 = db.Column(db.String)
	email = db.Column(db.String)
	date_added = db.Column(db.DateTime)
	ip = db.Column(db.String)


	def __init__(self, q1, q2, session_id):
		self.session_id = session_id
		self.q1 = q1
		self.q2 = q2
