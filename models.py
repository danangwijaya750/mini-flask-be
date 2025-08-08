from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(User(username="user1", password="password123"))
    db.session.add(User(username="user2", password="password321"))
    db.session.commit()
