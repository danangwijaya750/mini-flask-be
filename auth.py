from flask import Blueprint, request, jsonify, current_app
from models import User, db
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)

def generate_token(username, is_refresh=False):
    exp_seconds = 300 if is_refresh else 60  # 5 min ref. 1 min acc
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds),
        "refresh": is_refresh
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

def verify_token(token, expect_refresh=False):
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        if decoded.get("refresh") != expect_refresh:
            return None
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username"), password=data.get("password")).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = generate_token(user.username, is_refresh=False)
    refresh_token = generate_token(user.username, is_refresh=True)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token})

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    decoded = verify_token(refresh_token, expect_refresh=True)
    if not decoded:
        return jsonify({"error": "Invalid or expired refresh token"}), 401

    new_access = generate_token(decoded["sub"], is_refresh=False)
    new_refresh = generate_token(decoded["sub"], is_refresh=True)
    return jsonify({"access_token": new_access, "refresh_token": new_refresh})
