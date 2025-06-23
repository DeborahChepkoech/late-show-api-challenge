from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity 
from datetime import datetime

from server.models.__init__ import db
from server.models.episode import Episode

episode_bp = Blueprint('episodes', __name__)

@episode_bp.route('/', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

@episode_bp.route('/', methods=['POST'])
def create_episode():
    data = request.get_json()
    date_str = data.get('date')
    number = data.get('number')

    if not date_str or not number:
        return jsonify({"msg": "Date and number are required"}), 400

    try:
        episode_date = datetime.strptime(date_str, '%Y-%m-%d') 
        number = int(number)
    except ValueError:
        return jsonify({"msg": "Invalid date format (useYYYY-MM-DD) or invalid number"}), 400

    if Episode.query.filter_by(number=number).first():
        return jsonify({"msg": "Episode with this number already exists"}), 409

    new_episode = Episode(date=episode_date, number=number)
    try:
        db.session.add(new_episode)
        db.session.commit()
        return jsonify(new_episode.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error creating episode", "error": str(e)}), 500

@episode_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required() 
def delete_episode(id):
    current_user_id = get_jwt_identity()

    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"msg": "Episode not found"}), 404

    try:
        db.session.delete(episode)
        db.session.commit()
        return jsonify({"msg": f"Episode {id} and its appearances deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error deleting episode", "error": str(e)}), 500