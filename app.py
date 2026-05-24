from flask import Flask
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
  join_date   = db.Column(db.Date, nullable=False)
  created_at  = db.Column(db.DateTime, default=datetime.now)

@app.route("/")
def home():
    return "Flask + MySQL connected successfully!"


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