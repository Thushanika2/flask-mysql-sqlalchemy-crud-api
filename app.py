from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root123@localhost/my_school"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def home():
    return "Flask + MySQL connected successfully!"


if __name__ == '__main__':

    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            print("SUCCESS: Database connected successfully!")

    except Exception as e:
        print(f"ERROR: Database connection failed {e}")

    app.run(debug=True, port=7777)