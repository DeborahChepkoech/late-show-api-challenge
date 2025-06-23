from flask import Blueprint, jsonify, request

from server.models.__init__ import db
from server.models.guest import Guest

guest_bp = Blueprint('guests', __name__)

@guest_bp.route('/', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@guest_bp.route('/', methods=['POST'])

def create_guest():
    data = request.get_json()
    name = data.get('name')
    occupation = data.get('occupation')

    if not name:
        return jsonify({"msg": "Guest name is required"}), 400

    new_guest = Guest(name=name, occupation=occupation)
    try:
        db.session.add(new_guest)
        db.session.commit()
        return jsonify(new_guest.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error creating guest", "error": str(e)}), 500

@guest_bp.route('/<int:id>', methods=['GET'])
def get_guest_by_id(id):
    guest = Guest.query.get(id)
    if not guest:
        return jsonify({"msg": "Guest not found"}), 404
    return jsonify(guest.to_dict())

@guest_bp.route('/<int:id>', methods=['DELETE'])
def delete_guest(id):
    guest = Guest.query.get(id)
    if not guest:
        return jsonify({"msg": "Guest not found"}), 404
    try:
        db.session.delete(guest)
        db.session.commit()
        return jsonify({"msg": "Guest deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error deleting guest", "error": str(e)}), 500