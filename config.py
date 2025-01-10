import os, secrets
from dotenv import load_dotenv

base_dir: str = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class config:
    QUART_APP: str = os.environ.get('QUART_APP')
    ENV: str = os.environ.get('ENV')
    DEBUG: bool = os.environ.get('DEBUG').lower() == 'true'
    UPLOAD_FOLDER: str = os.environ.get('UPLOAD_FOLDER')
    SECRET_KEY: str = os.urandom(32)
    SESSION_COOKIE_SECURE: bool = os.environ.get('SESSION_COOKIE_SECURE').lower() == 'true'
    SESSION_COOKIE_HTTPONLY: bool = os.environ.get('SESSION_COOKIE_HTTPONLY').lower() == 'true'
    SESSION_COOKIE_SAMESITE: str = os.environ.get('SESSION_COOKIE_SAMESITE')
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS').lower() == 'true'
    QUART_AUTH_COOKIE_HTTP_ONLY: bool = os.environ.get('QUART_AUTH_COOKIE_HTTP_ONLY').lower() == 'true'
    QUART_AUTH_COOKIE_SECURE: bool = os.environ.get('QUART_AUTH_COOKIE_SECURE').lower() == 'true'
    QUART_AUTH_COOKIE_SAMESITE: str = os.environ.get('QUART_AUTH_COOKIE_SAMESITE')
    QUART_AUTH_DURATION:int = int(os.environ.get('QUART_AUTH_DURATION'))
    QUART_AUTH_SALT: str = secrets.token_urlsafe(16)
    
    # QUART_DB_DATABASE_URL = os.environ.get('QUART_DB_DATABASE_URL')
    # QUART_DB_MIGRATIONS_FOLDER = os.environ.get('QUART_DB_MIGRATIONS_FOLDER')
    # QUART_DB_STATE_TABLE_NAME = os.environ.get('QUART_DB_STATE_TABLE_NAME')
    # QUART_DB_DATA_PATH = os.environ.get('QUART_DB_DATA_PATH')
    # REDIS_STORE = os.environ.get('REDIS_STORE')
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_TLS = True
    # MAIL_PORT = 465
