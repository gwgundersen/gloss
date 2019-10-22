"""Configure and start the web server."""

import os
from flask import Flask, session as flask_session, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from gloss.config import config


""" Database configuration and app initialization
    -----------------------------------------------------------------------"""
# Create db first. Models all import this.
db = SQLAlchemy()

# Import models. They must be interpreted before creating the database.
from gloss import models

app = Flask(__name__,
            static_url_path="%s/static" % config.get("url", "base"),
            static_folder=config.get('folder', 'static'))

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:3306/%s" % (
    config.get("db", "user"),
    config.get("db", "passwd"),
    config.get("db", "host"),
    config.get("db", "db")
)
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800  # Recycle every 30 min.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()


""" URL configuration
    -----------------------------------------------------------------------"""
app.config.base_tag_url = config.get('url', 'base') + '/'


""" Debugging
    -----------------------------------------------------------------------"""
# It's impossible to debug a 500 error in production without seeing an error
# message.
app.config["DEBUG"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True


""" Server endpoints
    -----------------------------------------------------------------------"""
from gloss import endpoints
app.register_blueprint(endpoints.jinjafilters)
app.register_blueprint(endpoints.gloss_blueprint)
app.register_blueprint(endpoints.index_blueprint)
app.register_blueprint(endpoints.label_blueprint)
app.register_blueprint(endpoints.author_blueprint)
app.register_blueprint(endpoints.entity_blueprint)
app.register_blueprint(endpoints.auth_blueprint)
app.register_blueprint(endpoints.public_blueprint)
app.register_blueprint(endpoints.image_blueprint)


""" Login session management
    -----------------------------------------------------------------------"""
# Change this key to force all users to re-authenticate.
app.secret_key = config.get("cookies", "secret_key")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(models.User).get(user_id)
    return user


@app.before_request
def make_session_permanent():
    """Sets Flask session to "permanent", meaning 31 days."""
    flask_session.permanent = True


""" Error handling
    -----------------------------------------------------------------------"""
@app.errorhandler(404)
def page_not_found(e):
    """Handles all 404 requests."""
    return render_template("error/404.html")


@app.errorhandler(405)
def method_not_allowed(e):
    """Handles all 405 requests."""
    return render_template("error/405.html")


""" Pandoc configuration
    -----------------------------------------------------------------------"""
# Set binary location for pandoc. This is important because Flask and Apache
# both run as special users and cannot find the binaries otherwise.
os.environ.setdefault("PYPANDOC_PANDOC", config.get("path", "pandoc"))
if not config.getboolean("mode", "debug"):
    os.environ.setdefault("HOME", config.get("path", "home"))
    os.environ.setdefault("LD_LIBRARY_PATH", config.get("path", "ld_library"))
