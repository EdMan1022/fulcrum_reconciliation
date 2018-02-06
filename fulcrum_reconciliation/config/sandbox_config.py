from .base_config import BaseConfig
import os


class SandboxConfig(BaseConfig):

    API_KEY = os.environ.get('FULCRUM_SANDBOX_API_KEY')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')