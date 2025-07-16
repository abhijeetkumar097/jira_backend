from models.user import User
from models.login import Login 
from models.role import Role
from models import db 

def create_user(username, email, first_name, last_name, password):
    new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user_role = Role.query.filter_by(name='user').first()
    new_user.roles.append(user_role)
    db.session.add(new_user)
    db.session.commit()
    new_login = Login(user_id=new_user.id, password=password)
    db.session.add(new_login)
    db.session.commit()
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user
def get_user_by_id(id):
    user = User.query.get(id)
    return user
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user
def check_user_password(user, password):
    if not user:
        return False
    login_entry = Login.query.filter_by(user_id=user.id).first()
    if login_entry and login_entry.password == password:
        return True 
    return False

def create_super_admin(username, email, password):
    new_user = User(username = username, email = email)
    super_role = Role.query.filter_by(name='super_admin').first()
    new_user.roles.append(super_role)
    db.session.add(new_user)
    db.session.commit()
    new_login = Login(user_id = new_user.id, password = password)
    db.session.add(new_login)
    db.session.commit()

def assign_role(username, role):
    user = User.query.filter_by(username = username).first()
    new_role = Role.query.filter_by(name = role).first()
    if new_role not in user.roles:
        user.roles.append(new_role)
        db.session.commit()

def get_all_users():
    users = User.query.all()


def get_user_overview(user_id):
    user = User.query.get_or_404(user_id)

    user_projects = [project.to_dict() for project in user.projects]
    user_teams = []
    for team in user.teams:
        user_teams.append({
            "team_id": team.team_id,
            "team_name": team.team_name,
            "description": team.description,
            "members": [{"id": member.id, "username": member.username, "email": member.email} for member in team.members]
        })

    return {
        "projects": user_projects,
        "teams": user_teams
    }
