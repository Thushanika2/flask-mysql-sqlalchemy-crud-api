from flask import request, jsonify

from app.config import db
from app.models.course_model import Course


def create_course():

    data = request.get_json()

    if not data:
        return jsonify({"ERROR": "Request body is empty"}), 400

    if not data.get("course_title"):
        return jsonify({"ERROR": "Course title is required"}), 400

    existing_title = Course.query.filter_by(course_title=data["course_title"]).first()

    if existing_title:
        return jsonify({"ERROR": "Course title already exists"}), 400

    if not data.get("course_fee"):
        return jsonify({"ERROR": "Course fee is required"}), 400

    if data["course_fee"] <= 0:
        return jsonify({"ERROR": "Course fee must be a positive number"}), 400

    if not data.get("duration_months"):
        return jsonify({"ERROR": "Duration months is required"}), 400

    if data["duration_months"] <= 0:
        return jsonify({"ERROR": "Duration months must be a positive number"}), 400

    try:
        new_course = Course(
            course_title    = data["course_title"],
            course_fee      = data["course_fee"],
            duration_months = data["duration_months"],
            description     = data.get("description"),
            is_available    = data.get("is_available", True),
        )

        db.session.add(new_course)
        db.session.commit()

        return jsonify({"MESSAGE": "Created Course Successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def get_courses():

    try:
        courses = Course.query.all()

        if not courses:
            return jsonify({"ERROR": "Course is not found"}), 404

        course_detail = []

        for course in courses:
            course_detail.append({
                "id"              : course.id,
                "course_title"    : course.course_title,
                "course_fee"      : course.course_fee,
                "duration_months" : course.duration_months,
                "description"     : course.description,
                "is_available"    : course.is_available,
                "created_at"      : course.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return jsonify(course_detail), 200

    except Exception as e:
        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def get_course(id):

    try:
        course = Course.query.get(id)

        if not course:
            return jsonify({"ERROR": "Course is not found"}), 404

        return jsonify({
            "id"              : course.id,
            "course_title"    : course.course_title,
            "course_fee"      : course.course_fee,
            "duration_months" : course.duration_months,
            "description"     : course.description,
            "is_available"    : course.is_available,
            "created_at"      : course.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    except Exception as e:
        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def update_course(id):

    course = Course.query.get(id)

    if not course:
        return jsonify({"ERROR": "Course is not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"ERROR": "Data is not found"}), 404

    try:
        course.course_title    = data.get("course_title",    course.course_title)
        course.course_fee      = data.get("course_fee",      course.course_fee)
        course.duration_months = data.get("duration_months", course.duration_months)
        course.description     = data.get("description",     course.description)
        course.is_available    = data.get("is_available",    course.is_available)

        db.session.commit()

        return jsonify({"MESSAGE": "Course updated successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def delete_course(id):

    course = Course.query.get(id)

    if not course:
        return jsonify({"ERROR": "Course is not found"}), 404

    try:
        db.session.delete(course)
        db.session.commit()

        return jsonify({"MESSAGE": "Course deleted successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500
