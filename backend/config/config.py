import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'default_secret')
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

class DevelopmentConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True

class ProductionConfig(Config):
    DEBUG: bool = False
    SQLALCHEMY_ECHO: bool = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}