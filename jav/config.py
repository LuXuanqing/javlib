import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret thing')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = '0.0.0.0'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'data.db')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'data_dev.db')
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class BotConfig(object):
    domain_url = 'https://www.javbus.com'
    proxy = {
        'http': 'http://localhost:7890',
        'https': 'http://localhost:7890',
    }
    enable_proxy = True
    timeout = 5

