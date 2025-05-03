from flask import Flask
from flask_cors import CORS 
from .routes.students import students_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(students_bp, url_prefix='/students')
    return app
