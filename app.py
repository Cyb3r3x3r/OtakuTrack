from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import datetime

#initializing extensions
db = SQLAlchemy()
loginManager = LoginManager()


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-secret')

    # ensure instance folder exists
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)

    # correct database path
    db_path = os.path.join(app.instance_path, 'otakutrack.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    loginManager.init_app(app)
    loginManager.login_view = 'auth.login'

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from anime import anime as anime_blueprint
    app.register_blueprint(anime_blueprint)
    @app.context_processor
    def inject_year():
        return {"current_year": datetime.now().year}
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("403.html"), 403

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    return app

