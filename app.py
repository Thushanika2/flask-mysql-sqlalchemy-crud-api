from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root123@localhost/my_school"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Student(db.Model):

  __tablename__ = 'students'

  id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
  full_name   = db.Column(db.String(100), nullable=False)
  email       = db.Column(db.String(120), unique=True, nullable=False)
  age         = db.Column(db.Integer, nullable=False)
  cgpa        = db.Column(db.Float, nullable=False,default=0.0)
  is_active   = db.Column(db.Boolean, default=True)
  joined_date = db.Column(db.Date, nullable=False)
  created_at  = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    return "Flask + MySQL connected successfully!"


@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()

    try:
        new_student    = Student(
            full_name  =data['full_name'],
            email      =data['email'],
            age        =data['age'],
            cgpa       =data.get('cgpa',0.0),
            is_active  =data.get('is_active', True),
            joined_date=datetime.strptime(data['joined_date'],'%Y-%m-%d')
        )

        db.session.add(new_student)
        db.session.commit()
        return jsonify({'MESSAGE': 'Created Student Successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'ERROR': str(e)}), 400


if __name__ == '__main__':

    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            print("SUCCESS: Database connected successfully!")

            try:
               db.create_all()
               print("SUCCESS: Tables created successfully!")

            except Exception as e:
               print(f"ERROR: Table creation failed {e}")

    except Exception as e:
         print(f"ERROR: Database connection failed {e}")

    app.run(debug=True, port=7777)