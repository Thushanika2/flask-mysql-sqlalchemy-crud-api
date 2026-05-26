from sqlalchemy import text

from app.config import create_app, db

app = create_app()

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
