import os

class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = '43DK&$GBV$MSHY'
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/vidcon"
	DEBUG = False


class ProductionConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
	TESTING = True

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
	TESTING = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
	TESTING = True

class TestingConfig(Config):
	TESTING = True
