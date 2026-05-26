import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


class Config:

    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST     = os.getenv("DB_HOST")
    DB_NAME     = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI        = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.student_routes import student_bp
    from app.routes.course_routes import course_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    @app.route("/")
    def home():
        return "Flask + MySQL connected successfully!"

    import app.models.student_model  # noqa: F401
    import app.models.course_model   # noqa: F401

    return app
