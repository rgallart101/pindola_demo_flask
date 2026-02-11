import os
from flask import Flask, session, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_babel import Babel, gettext as _

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
babel = Babel()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists (for SQLite db)
    os.makedirs(app.instance_path, exist_ok=True)

    # Config
    from .config import Config
    app.config.from_object(Config())
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
    # Use absolute path for translations
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(os.path.dirname(__file__), 'translations')

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Define locale selector function
    def select_locale():
        """Select locale: session > browser preference > default"""
        if 'locale' in session:
            return session['locale']
        return request.accept_languages.best_match(['ca', 'en']) or 'en'

    # Register with Babel
    babel.init_app(app, locale_selector=select_locale)

    # Make select_locale available in templates
    app.jinja_env.globals.update(get_locale=select_locale)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Blueprints
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    # DB init
    with app.app_context():
        from .models import User
        db.create_all()

    return app

