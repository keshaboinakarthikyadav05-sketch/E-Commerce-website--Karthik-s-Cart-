import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError

# Load .env from backend directory or workspace root
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(backend_dir, '.env')
if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)
else:
    load_dotenv()

class Config:
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development').lower()
    IS_PRODUCTION = ENVIRONMENT == 'production' or os.getenv('RENDER', '').lower() == 'true'

    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if IS_PRODUCTION and (not SECRET_KEY or not JWT_SECRET_KEY):
        raise RuntimeError('Set SECRET_KEY and JWT_SECRET_KEY in the production environment.')
    SECRET_KEY = SECRET_KEY or secrets.token_urlsafe(32)
    JWT_SECRET_KEY = JWT_SECRET_KEY or secrets.token_urlsafe(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    raw_db_url = os.getenv('DATABASE_URL')
    if raw_db_url is None:
        if IS_PRODUCTION:
            raise RuntimeError(
                'DATABASE_URL is required in production. Connect a Render PostgreSQL '
                'database in the service environment.'
            )
        sqlite_path = os.path.join(backend_dir, 'shopora.db')
        raw_db_url = URL.create('sqlite', database=sqlite_path).render_as_string(hide_password=False)
    else:
        raw_db_url = raw_db_url.strip()
        if not raw_db_url:
            raise RuntimeError(
                'DATABASE_URL is set but empty. In Render, set it to the database '
                'internal connection string or apply the repository render.yaml Blueprint.'
            )

    # Render provides postgres:// URLs; SQLAlchemy needs postgresql+psycopg2://.
    if raw_db_url.startswith('postgres://'):
        raw_db_url = raw_db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    # Ensure psycopg2 driver is specified if generic postgresql:// is provided
    if raw_db_url.startswith('postgresql://'):
        raw_db_url = raw_db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

    try:
        parsed_db_url = make_url(raw_db_url)
    except ArgumentError as error:
        raise RuntimeError(
            'DATABASE_URL is not a valid SQLAlchemy URL. Set it to a SQLite or PostgreSQL '
            'connection URL.'
        ) from error
    if parsed_db_url.get_backend_name() not in ('sqlite', 'postgresql'):
        raise RuntimeError('DATABASE_URL must use SQLite or PostgreSQL.')
    
    SQLALCHEMY_DATABASE_URI = raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTO_INITIALIZE_DATABASE = True
    
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
    
    CORS_HEADERS = 'Content-Type'
