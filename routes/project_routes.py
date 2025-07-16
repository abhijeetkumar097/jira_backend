
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.project_controller import (
    create_project, update_project, get_user_projects, get_project_with_stats,
    delete_project, get_all_projects
)
from controllers.task_controller import get_project_tasks_by_status

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@projects_bp.route('/', methods=['GET'])
@jwt_required()
def list_projects():
    user_id = int(get_jwt_identity())
    projects = get_user_projects(user_id)
    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route('/new', methods=['POST'])
@jwt_required()
def new_project():
    user_id = get_jwt_identity()
    data = request.get_json()
    project = create_project(data, user_id)
    return jsonify(project.to_dict()), 201


@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def view_project(project_id):
    project, stats = get_project_with_stats(project_id)
    return jsonify({
        'project': project.to_dict(),
        'stats': stats
    }), 200


@projects_bp.route('/<int:project_id>/board', methods=['GET'])
@jwt_required()
def kanban_board(project_id):
    print(project_id)
    project, stats = get_project_with_stats(project_id)
    task_board = get_project_tasks_by_status(project_id)
    return jsonify({
        'project': project.to_dict(),
        'stats': stats,
        'task_board': {
            k: [t.to_dict() for t in v] for k, v in task_board.items()
        }
    }), 200


@projects_bp.route('/<int:project_id>/edit', methods=['PUT'])
@jwt_required()
def edit_project(project_id):
    data = request.get_json()
    project = update_project(project_id, data)
    return jsonify(project.to_dict()), 200


@projects_bp.route('/<int:project_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_project_route(project_id):
    delete_project(project_id)
    return jsonify({'message': 'Project deleted successfully.'}), 200
