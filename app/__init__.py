from flask import Flask
from .routes.students import students_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(students_bp, url_prefix='/students')
    return app
