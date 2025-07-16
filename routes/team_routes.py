from flask import Blueprint, request, jsonify
from controllers.team_controller import create_team, get_all_teams
from flask_jwt_extended import jwt_required

team_bp = Blueprint('team_bp', __name__, url_prefix='/api/teams')

@team_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    team = create_team(data)
    return jsonify(team.to_dict()), 201

@team_bp.route('/', methods=['GET'])
@jwt_required()
def get_teams():
    teams = get_all_teams()
    # return jsonify([t.to_dict() for t in teams]), 200
    return jsonify([{'team_id': t.team_id, 'team_name': t.team_name} for t in teams]), 200