from flask import Flask

from app.config import Config, db


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

    from .models import student_model  # noqa: F401
    from .models import course_model   # noqa: F401

    return app
