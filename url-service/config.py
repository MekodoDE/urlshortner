class Config(object):
    DEBUG = False
    TESTING = False
    API_VERSION = 0.1
    API_TITLE = 'url-service'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CORS_ORIGINS = ["*"]
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@127.0.0.1/urls'
class DevelopmentConfig(Config):
    DEBUG = True