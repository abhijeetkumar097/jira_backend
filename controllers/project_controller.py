# from models.project import Project
# from models.user import User
# from models.task import Task
# from models import db
# from sqlalchemy import func

# def create_project(data, user_id):
#     project = Project(
#         project_name=data.get("project_name"),
#         project_key=data.get("project_key", "").upper(),
#         description=data.get("description"),
#         project_link=data.get("project_link"),
#         status=data.get("status", "active")
#     )
#     db.session.add(project)
#     db.session.commit()

#     # Add the creator to the project
#     creator = User.query.get(user_id)
#     project.users.append(creator)

#     # Add other selected users
#     for uid in data.get("users", []):
#         user = User.query.get(uid)
#         if user and user not in project.users:
#             project.users.append(user)

#     db.session.commit()
#     return project


# def update_project(project_id, data):
#     project = Project.query.get_or_404(project_id)
#     project.project_name = data.get("project_name")
#     project.project_key = data.get("project_key", "").upper()
#     project.description = data.get("description")
#     project.project_link = data.get("project_link")
#     project.status = data.get("status", "active")

#     project.users.clear()
#     for uid in data.get("users", []):
#         user = User.query.get(uid)
#         if user:
#             project.users.append(user)

#     db.session.commit()
#     return project


# def get_user_projects(user_id):
#     user = User.query.get(user_id)
#     return user.projects if user else []

# def get_project_with_stats(project_id):
#     project = Project.query.get_or_404(project_id)
#     task_stats = db.session.query(
#         Task.status,
#         func.count(Task.id).label('count')
#     ).filter_by(project_id=project_id, is_deleted=False).group_by(Task.status).all()
    
#     stats = {status: count for status, count in task_stats}
#     total_tasks = Task.query.filter_by(project_id=project_id, is_deleted=False).count()
#     from datetime import date
#     overdue_tasks = Task.query.filter(
#         Task.project_id == project_id,
#         Task.is_deleted == False,
#         Task.due_date < date.today(),
#         Task.status != 'done'
#     ).count()
    
#     stats['total'] = total_tasks
#     stats['overdue'] = overdue_tasks
    
#     return project, stats

# def delete_project(project_id):
#     project = Project.query.get_or_404(project_id)
#     project.is_deleted = True
#     db.session.commit()

# def get_all_projects():
#     return Project.query.filter_by(is_deleted=False).all()



from models.project import Project
from models.user import User
from models.task import Task
from models.team import Team
from models import db
from sqlalchemy import func
from datetime import date


def create_project(data, user_id):
    project = Project(
        project_name=data.get("project_name"),
        description=data.get("description"),
        project_link=data.get("project_link"),
        status=data.get("status", "active")
    )
    db.session.add(project)
    db.session.commit()

    # Add teams to project
    for tid in data.get("teams", []):
        team = Team.query.get(tid)
        if team:
            project.teams.append(team)
            # Add all users in this team to the project's users list
            for member in team.members:
                if member not in project.users:
                    project.users.append(member)

    # Also add the creator of the project (if not already)
    creator = User.query.get(user_id)
    if creator and creator not in project.users:
        project.users.append(creator)


    db.session.commit()
    return project



def update_project(project_id, data):
    project = Project.query.get_or_404(project_id)
    project.project_name = data.get("project_name")
    project.project_key = data.get("project_key", "").upper()
    project.description = data.get("description")
    project.project_link = data.get("project_link")
    project.status = data.get("status", "active")

    project.teams.clear()
    for tid in data.get("teams", []):
        team = Team.query.get(tid)
        if team:
            project.teams.append(team)

    db.session.commit()
    return project


def get_user_projects(user_id):
    user = User.query.get(user_id)
    return user.projects if user else []


def get_project_with_stats(project_id):
    project = Project.query.get_or_404(project_id)
    task_stats = db.session.query(
        Task.status,
        func.count(Task.id).label('count')
    ).filter_by(project_id=project_id, is_deleted=False).group_by(Task.status).all()

    stats = {status: count for status, count in task_stats}
    total_tasks = Task.query.filter_by(project_id=project_id, is_deleted=False).count()
    overdue_tasks = Task.query.filter(
        Task.project_id == project_id,
        Task.is_deleted == False,
        Task.due_date < date.today(),
        Task.status != 'done'
    ).count()
    print(total_tasks)
    stats['total'] = total_tasks
    stats['overdue'] = overdue_tasks

    return project, stats


def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.is_deleted = True
    db.session.commit()


def get_all_projects():
    return Project.query.filter_by(is_deleted=False).all()
