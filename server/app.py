from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

from server.models.__init__ import db
from server.models.user import User
from server.models.guest import Guest
from server.models.episode import Episode
from server.models.appearance import Appearance

from server.controllers.auth_controller import auth_bp
from server.controllers.guest_controller import guest_bp
from server.controllers.episode_controller import episode_bp
from server.controllers.appearance_controller import appearance_bp


migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')


    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "a-very-secret-key-that-you-should-change-in-prod")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 3600))


    db.init_app(app) 
    migrate.init_app(app, db)
    jwt = JWTManager(app) 


    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(guest_bp, url_prefix='/api/guests')
    app.register_blueprint(episode_bp, url_prefix='/api/episodes')
    app.register_blueprint(appearance_bp, url_prefix='/api/appearances')

   
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Late Show API!"})


    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Guest': Guest,
            'Episode': Episode,
            'Appearance': Appearance
        }

    return app

if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run(debug=True)