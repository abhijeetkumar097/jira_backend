
from .main_routes import main_bp
from .user_routes import user_bp
from .task_routes import tasks_bp
from .project_routes import projects_bp
from .post_routes import post_bp
from .team_routes import team_bp
from .activity_routes import activity_bp
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(activity_bp)