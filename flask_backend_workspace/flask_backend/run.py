from app import app
from app.models import db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the DB is initialized
    # To (re)initialize the DB, delete flask_backend_workspace/flask_backend/app.db and restart.
    app.run(host="0.0.0.0", port=5000)
