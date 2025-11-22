from flask import Flask
from flask_migrate import Migrate
from .config import db

# models are defined in other modules, thus must be imported
# before calling create_all, otherwise SQLAlchemy will not know about them
# https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/
from .models import (
    SIEMLogsDBtable,
    SIEMLogsFileDBProperties
)
from .routes import siem_route_view_bp
from .generate_logs import generate_network_server_logs
from .network_folder_access import SIEMNetworkFolderAccess
import os

migrate = Migrate()
SIEM_LOGS_DIRECTORY ='SIEM_logs'

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) 

    flask_env = os.getenv("FLASK_ENV", "production")
    if flask_env == "production":
        app.config.from_object("flask_sse_with_logs.settings_prod")
    elif flask_env == "development":
        app.config.from_object("flask_sse_with_logs.settings_dev")

    db.init_app(app)

    # database migration
    migrate.init_app(app, db)

    # register view blueprints
    _register_blueprints(app)

    # create table schema in database
    _create_db_tables(app,db)

    # generate and write log to (SIEM_logs) directory on application startup
    generate_network_server_logs()

    return app 


def _create_db_tables(app, db):
    with app.app_context():
        db.create_all()

def _register_blueprints(app):
    app.register_blueprint(siem_route_view_bp)