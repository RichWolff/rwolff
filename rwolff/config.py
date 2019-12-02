class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testDB.sqlite'

class ProductionConfig(Config):
    DATABASE_URI = 'richwolff-1160.postgres.pythonanywhere-services.com'
    u = 'richwolff'
    p = '97a101e105i*'
    port = '11160'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{:}:{:}@{:}:{:}/wolff'.format(u, p, DATABASE_URI, port)

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
