from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_login import LoginManager

app = Flask(__name__)

from config import os, DevelopmentConfig, ProductionConfig

if os.environ.get('LOCAL'):
	app.config.from_object(DevelopmentConfig)
else:
	app.config.from_object(ProductionConfig)

# Initiate LoginManager
login_manager = LoginManager(app)
# Tells flask_login which view function will handle the login, convenient to force users to be logged to access certain views
login_manager.login_view = 'login'

# Initiate db instance
db = SQLAlchemy(app)
# Initiatie Migrate
migrate = Migrate(app, db)

from app import views
