from fulcrum_reconciliation.app import create_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from fulcrum_reconciliation.config import ProductionConfig


app = create_app(config=ProductionConfig)

from fulcrum_reconciliation.extensions import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
