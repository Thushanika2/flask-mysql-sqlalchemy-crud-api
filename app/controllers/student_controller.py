from flask import request, jsonify
from app.config import db
from app.models.student_model import Student
from datetime import datetime


def create_student():

    data = request.get_json()

    if not data:
        return jsonify({"ERROR": "Request body is empty"}), 400

    if not data.get("full_name"):
        return jsonify({"ERROR": "Full name is required"}), 400

    if not data.get("email"):
        return jsonify({"ERROR": "Email is required"}), 400

    existing_email = Student.query.filter_by(email=data["email"]).first()

    if existing_email:
        return jsonify({"ERROR": "Email already exists"}), 400

    if not data.get("age"):
        return jsonify({"ERROR": "Age is required"}), 400

    if data["age"] <= 0:
        return jsonify({"ERROR": "Age must be a positive number"}), 400

    if not data.get("joined_date"):
        return jsonify({"ERROR": "Joined date is required"}), 400

    try:
        joined_date = datetime.strptime(data["joined_date"], "%Y-%m-%d").date()

    except:
        return jsonify({"ERROR": "Joined date format must be YYYY-MM-DD"}), 400

    if "cgpa" in data:
        if data["cgpa"] < 0:
            return jsonify({"ERROR": "CGPA cannot be negative"}), 400

    try:
        new_student = Student(

            full_name   = data["full_name"],
            email       = data["email"],
            age         = data["age"],
            cgpa        = data.get("cgpa", 0.0),
            is_active   = data.get("is_active", True),
            joined_date = joined_date

        )

        db.session.add(new_student)
        db.session.commit()

        return jsonify({"MESSAGE": "Created Student Successfully!"}), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def get_students():

    try:
        students = Student.query.all()

        if not students:
            return jsonify({"ERROR": "Student is not found"}), 404

        student_detail = []

        for student in students:

            student_detail.append({

                "id"         : student.id,
                "full_name"  : student.full_name,
                "email"      : student.email,
                "age"        : student.age,
                "cgpa"       : student.cgpa,
                "is_active"  : student.is_active,
                "joined_date": student.joined_date.strftime("%Y-%m-%d"),
                "created_at" : student.created_at.strftime("%Y-%m-%d %H:%M:%S")

            })

        return jsonify(student_detail), 200

    except Exception as e:

        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def get_student(id):

    try:
        student = Student.query.get(id)

        if not student:
            return jsonify({"ERROR": "Student is not found"}), 404

        return jsonify({

            "id"         : student.id,
            "full_name"  : student.full_name,
            "email"      : student.email,
            "age"        : student.age,
            "cgpa"       : student.cgpa,
            "is_active"  : student.is_active,
            "joined_date": student.joined_date.strftime("%Y-%m-%d"),
            "created_at" : student.created_at.strftime("%Y-%m-%d")

        })

    except Exception as e:

        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def update_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({"ERROR": "Student is not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"ERROR": "Data is not found"}), 404

    try:

        student.full_name   = data.get("full_name",   student.full_name)
        student.email       = data.get("email",       student.email)
        student.age         = data.get("age",         student.age)
        student.cgpa        = data.get("cgpa",        student.cgpa)
        student.is_active   = data.get("is_active",   student.is_active)
        student.joined_date = data.get("joined_date", student.joined_date)

        db.session.commit()

        return jsonify({"MESSAGE": "Student updated successfully!"})

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500


def delete_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({"ERROR": "Student is not found"}), 404

    try:

        db.session.delete(student)
        db.session.commit()

        return jsonify({"MESSAGE": "Student deleted successfully!"})

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR": "Internal server error", "details": str(e)}), 500