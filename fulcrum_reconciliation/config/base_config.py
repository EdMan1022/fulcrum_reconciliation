import os
import dotenv

# Load in any environment variables
env_path = os.path.join(os.getcwd(), '.env')
dotenv.load_dotenv(env_path)


class BaseConfig(object):
    """
    Wraps the base configuration for the app
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_PRODUCTION_DATABASE_URI')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False