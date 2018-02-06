from flask import Flask
from .extensions import db
from .config.base_config import BaseConfig
import fulcrum_reconciliation.exceptions as exc

def create_app(config: BaseConfig):

    if config is None:
        raise exc.NoAppConfigError

