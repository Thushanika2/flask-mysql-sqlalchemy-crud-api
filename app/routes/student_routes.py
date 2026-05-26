from flask import Blueprint

from app.controllers import student_controller as controller

student_bp = Blueprint("student", __name__)


@student_bp.route("/api/students", methods=["POST"])
def create_student():
    return controller.create_student()


@student_bp.route("/api/students", methods=["GET"])
def get_students():
    return controller.get_students()


@student_bp.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):
    return controller.get_student(id)


@student_bp.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    return controller.update_student(id)


@student_bp.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    return controller.delete_student(id)
