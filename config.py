import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-does-not-need-to-be-changed'

class ProductionConfig(Config):
    NAME = "Production"
    DEBUG = False


class StagingConfig(Config):
    NAME = "STAGING"
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    NAME = "DEVELOPMENT"
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    NAME = "TESTING"
    TESTING = True
