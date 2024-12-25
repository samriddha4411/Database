from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Configure SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes , models

# setup console logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info("Flask App Startup")