from app import create_app
from app.db import db
from flask_jwt_extended import JWTManager

app = create_app()
jwt = JWTManager(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
