import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env from backend directory or workspace root
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(backend_dir, '.env')
if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)
else:
    load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'shopora-super-secret-jwt-key-development-2026')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'shopora-jwt-secret-key-development-2026')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    raw_db_url = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg2://postgres:postgres@localhost:5432/shopora_db'
    )
    # Ensure psycopg2 driver is specified if generic postgresql:// is provided
    if raw_db_url.startswith('postgresql://'):
        raw_db_url = raw_db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    
    SQLALCHEMY_DATABASE_URI = raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Razorpay Test Configuration
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_shopora12345')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'shopora_razorpay_secret_key_98765')
    
    CORS_HEADERS = 'Content-Type'
