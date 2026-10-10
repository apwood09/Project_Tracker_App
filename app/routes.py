from flask import Blueprint, jsonify, render_template, request

from .extensions import db
from .models import Item

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


@main_bp.route("/api/items", methods=["GET"])
def list_items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return jsonify([i.to_dict() for i in items])


@main_bp.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify(error="'name' is required"), 400
    item = Item(name=name, description=data.get("description", ""))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@main_bp.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id): 
    print (f"---> Delete route hit for item ID: {item_id} <---")
    item = Item.query.filter_by(id=item_id).first()

    if not item: 
        return jsonify({"error": f"Item {item_id} not found in database"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": f"Item {item_id} deleted succesfully"}), 200