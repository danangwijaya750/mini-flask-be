from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth import auth_bp
from models import db, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(auth_bp)

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
