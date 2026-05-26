from flask import Blueprint

from app.controllers import course_controller as controller

course_bp = Blueprint("course", __name__)


@course_bp.route("/api/courses", methods=["POST"])
def create_course():
    return controller.create_course()


@course_bp.route("/api/courses", methods=["GET"])
def get_courses():
    return controller.get_courses()


@course_bp.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):
    return controller.get_course(id)


@course_bp.route("/api/courses/<int:id>", methods=["PUT"])
def update_course(id):
    return controller.update_course(id)


@course_bp.route("/api/courses/<int:id>", methods=["DELETE"])
def delete_course(id):
    return controller.delete_course(id)
