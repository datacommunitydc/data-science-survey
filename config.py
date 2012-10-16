import os

class Config(object):
	DEBUG = False
	TESTING = False
	SECRET_KEY = '\xb7Fr\xbd7TQ\x7f9]\xafr\xf0\xa9\xe70Q\xbcY\xe8\xe8\x00v\xa6'
	CSRF_ENABLED = True
	#DATABASE_URI = 'sqlite:////tmp/badges.db'
	SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/badges.db'

class ProductionConfig(Config):
	if 'DATABASE_URL' in os.environ.keys():
		DATABASE_URI = os.environ['DATABASE_URL']
	#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True