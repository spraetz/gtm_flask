import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'this-really-does-not-need-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


class ProductionConfig(Config):
    NAME = "Production"


class StagingConfig(Config):
    NAME = "STAGING"
    DEVELOPMENT = True
    DEBUG = True

# Note, DevelopmentConfig is found in config_local.py (which is in .gitignore for security reasons)


class TestingConfig(Config):
    NAME = "TESTING"
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/gtm_testing"
    TESTING = True
    WTF_CSRF_ENABLED = False
