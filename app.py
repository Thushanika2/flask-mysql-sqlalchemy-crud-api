from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root123@localhost/my_school"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/")
def home():
    return "Flask + MySQL connected successfully!"


db = SQLAlchemy(app)


class Student(db.Model):

    __tablename__ = "students"

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name   = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    age         = db.Column(db.Integer, nullable=False)
    cgpa        = db.Column(db.Float, nullable=False,default=0.0)
    is_active   = db.Column(db.Boolean, default=True)
    joined_date = db.Column(db.Date, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)



class Course(db.Model):

    __tablename__ = "courses"

    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_title     = db.Column(db.String(100), unique=True, nullable=False)
    course_fee       = db.Column(db.Float, nullable=False)
    duration_months  = db.Column(db.Integer, nullable=False)
    description      = db.Column(db.Text, nullable=False)
    is_available     = db.Column(db.Boolean, default=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)



#POST METHOD (STUDENT)

@app.route("/api/students", methods=["POST"])
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
        joined_date = datetime.strptime(data["joined_date"],"%Y-%m-%d").date()

    except:

        return jsonify({"ERROR": "Joined date format must be YYYY-MM-DD"}), 400


    if "cgpa" in data:

        if data["cgpa"] < 0:

            return jsonify({"ERROR": "CGPA cannot be negative"}), 400


    try:
        new_student     = Student(

            full_name   = data["full_name"],
            email       = data["email"],
            age         = data["age"],
            cgpa        = data.get("cgpa",0.0),
            is_active   = data.get("is_active", True),
            joined_date = datetime.strptime(data["joined_date"],"%Y-%m-%d")

        )

        db.session.add(new_student)

        db.session.commit()

        return jsonify({"MESSAGE": "Created Student Successfully!"}), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500
    


#GET ALL STUDENTS

@app.route("/api/students", methods=["GET"])
def get_students():

    try:
        students= Student.query.all()

        student_detail=[]

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

        return jsonify(student_detail),200
    
    except Exception as e:

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500



#GET STUDENT BY ID

@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):

    try:
        student=Student.query.get(id)

        if not student:

            return jsonify({"ERROR": "Student is not found"}),404

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

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500



#UPDATE STUDENT BY ID(PUT)

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):

    student = Student.query.get(id)

    if not student:

        return jsonify({'ERROR': 'Student is not found'}), 404

    data = request.get_json()

    if not data:

        return jsonify({"ERROR": "Data is not found"}), 404

    try:

        student.full_name   = data.get('full_name',student.full_name)
        student.email       = data.get('email', student.email)
        student.age         = data.get('age', student.age)
        student.cgpa        = data.get('cgpa', student.cgpa)
        student.is_active   = data.get('is_active', student.is_active)
        student.joined_date = data.get('joined_date', student.joined_date)

        db.session.commit()

        return jsonify({'MESSAGE': 'Student updated successfully!'})

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500



#DELETE STUDENT BY ID (DELETE)

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    student = Student.query.get(id)

    if not student:

        return jsonify({'ERROR': 'Student is not found'}), 404

    try:

        db.session.delete(student)

        db.session.commit()

        return jsonify({'MESSAGE': 'Student deleted successfully!'})

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500



#POST METHOD (COURSE)

@app.route("/api/courses", methods=["POST"])
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
        new_course     = Course(

            course_title    = data["course_title"],
            course_fee      = data["course_fee"],
            duration_months = data["duration_months"],
            description     = data.get("description"),
            is_available    = data.get("is_available", True)

        )

        db.session.add(new_course)

        db.session.commit()

        return jsonify({"MESSAGE": "Created Course Successfully!"}), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500
    


#GET ALL COURSES

@app.route("/api/courses", methods=["GET"])
def get_courses():

    try:
        courses = Course.query.all()

        course_detail=[]

        for course in courses:

            course_detail.append({

                "id"              : course.id,
                "course_title"    : course.course_title,
                "course_fee"      : course.course_fee,
                "duration_months" : course.duration_months,
                "description"     : course.description,
                "is_available"    : course.is_available,
                "created_at"      : course.created_at.strftime("%Y-%m-%d %H:%M:%S")

            })

        return jsonify(course_detail),200
    
    except Exception as e:

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500
    


#GET COURSE BY ID

@app.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):

    try:
        course=Course.query.get(id)

        if not course:

            return jsonify({"ERROR": "Course is not found"}),404

        return jsonify({

                "id"              : course.id,
                "course_title"    : course.course_title,
                "course_fee"      : course.course_fee,
                "duration_months" : course.duration_months,
                "description"     : course.description,
                "is_available"    : course.is_available,
                "created_at"      : course.created_at.strftime("%Y-%m-%d %H:%M:%S")

        })

    except Exception as e:

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500



#UPDATE COURSE BY ID(PUT)

@app.route('/api/courses/<int:id>', methods=['PUT'])
def update_course(id):

    course = Course.query.get(id)

    if not course:

        return jsonify({'ERROR': 'Course is not found'}), 404

    data = request.get_json()

    if not data:

        return jsonify({"ERROR": "Data is not found"}), 404

    try:

        course.course_title     = data.get('course_title',course.course_title)
        course.course_fee       = data.get('course_fee', course.course_fee)
        course.duration_months  = data.get('duration_months', course.duration_months)
        course.description      = data.get('description', course.description)
        course.is_available     = data.get('is_available', course.is_available)

        db.session.commit()

        return jsonify({'MESSAGE': 'Course updated successfully!'}),201

    except Exception as e:

        db.session.rollback()

        return jsonify({"ERROR":"Internal server error","details":str(e)}), 500
       


if __name__ == "__main__":

    try:
        with app.app_context():

            db.session.execute(text("SELECT 1"))

            print({"SUCCESS": "Database connected successfully!"})


            try:
               db.create_all()

               print({"SUCCESS": "Tables created successfully!"})

            except Exception as e:
               
               print(f"ERROR: Table creation failed {e}")


    except Exception as e:
         
         print(f"ERROR: Database connection failed {e}")

    app.run(debug=True, port=7777)