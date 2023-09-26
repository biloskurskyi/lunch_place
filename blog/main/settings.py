"""This code helps configure the fundamental parameters of the application,
including the secret key and database connection parameters, using the .env file.
This allows confidential information to be stored separately from the code and protects it from unauthorized access."""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

SECRET_KEY = os.urandom(36)
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATION = os.environ.get('SQLALCHEMY_TRACK_MODIFICATION')
