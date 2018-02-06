from flask import Flask
from fulcrum_reconciliation.extensions import db
import fulcrum_reconciliation.exceptions as exc


def create_app(config):

    if config is None:
        raise exc.NoAppConfigError

    app = Flask(config.APP_NAME)
    app.config.from_object(config)

    db.init_app(app)
    db.app = app

    return app

