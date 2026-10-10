from flask import Blueprint, jsonify, render_template, request
from .extensions import db
from .models import Item, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/health")
def health():
    return jsonify(status="ok")

# Class User: GET 
@main_bp.route("/api/users", methods=["GET"])
def list_users(): 
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([i.to_dict() for i in users]), 200

# Class User: POST
@main_bp.route("/api/users", methods=["POST"])
def create_user(): 
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password")

    if not username or not password: 
        return jsonify(error=("'username' and 'password' are required")), 400
    
    # does user already exist? 
    if User.query.filter_by(username=username).first(): 
        return jsonify({"error": f"Username '{username} is already stitched"}), 400

    # initiate new user 
    new_user = User(username=username)
    new_user.set_password(password) #secure password hash 

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# Class User: DELETE
@main_bp.route("/api/users/<string:username>", methods=["DELETE"])
def delete_user(username): 
    user = User.query.filter_by(username=username).first()

    if not user: 
        return jsonify({"error": f"user {username} not seemed in database"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"user {username} succesfully unstitched"}), 200