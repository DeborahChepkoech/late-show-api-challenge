from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.models.__init__ import db
from server.models.appearance import Appearance
from server.models.guest import Guest 
from server.models.episode import Episode 

appearance_bp = Blueprint('appearances', __name__)

@appearance_bp.route('/', methods=['GET'])
def get_appearances():
    appearances = Appearance.query.all()
    return jsonify([app.to_dict() for app in appearances])

@appearance_bp.route('/', methods=['POST'])
@jwt_required() 
def create_appearance():
    current_user_id = get_jwt_identity()

    data = request.get_json()
    rating = data.get('rating')
    guest_id = data.get('guest_id')
    episode_id = data.get('episode_id')

    if not all([rating, guest_id, episode_id]):
        return jsonify({"msg": "Rating, guest_id, and episode_id are required"}), 400

    try:
        rating = int(rating)
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

    guest = Guest.query.get(guest_id)
    episode = Episode.query.get(episode_id)

    if not guest:
        return jsonify({"msg": "Guest not found"}), 404
    if not episode:
        return jsonify({"msg": "Episode not found"}), 404

    new_appearance = Appearance(rating=rating, guest_id=guest_id, episode_id=episode_id)

    try:
        db.session.add(new_appearance)
        db.session.commit()
        return jsonify(new_appearance.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error creating appearance", "error": str(e)}), 500