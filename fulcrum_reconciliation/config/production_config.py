from .base_config import BaseConfig
import os


class ProductionConfig(BaseConfig):
    """
    Config class for the live app
    """

    API_KEY = os.environ.get('FULCRUM_PRODUCTION_API_KEY')
