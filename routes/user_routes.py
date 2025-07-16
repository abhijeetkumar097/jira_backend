from flask import render_template, request, redirect, url_for, Blueprint, flash, jsonify
from controllers.user_controller import *
from form.user_form import RegistrationForm, LoginForm
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

    
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json
    username = data.get("username")
    lastname = data.get('lastname')
    email = data.get("email")
    password = data.get('password')
    confirm = data.get('confirm')
    print(data)
    if not username or not lastname or not email or not password or not confirm:
        return jsonify({'msg': 'All fields are required'}), 400
    if password != confirm:
        return jsonify({'msg', 'Passwords do not match'})
    if get_user_by_username(username):
        return jsonify({"msg" : 'Username already exists!'}), 401
    else:
        create_user(username, email, username, lastname, password)
        return jsonify({"msg" : 'Registration successful! Please login.'}), 200
        

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'Missing email or password'}), 400
    
    user = get_user_by_email(email)
    if user and check_user_password(user, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({ "token" : access_token})
    else:
        return jsonify({'msg' : "Invalid username or password"}), 401
    
@user_bp.route('/me/overview', methods=['GET'])
@jwt_required()
def user_overview():
    user_id = int(get_jwt_identity())
    overview = get_user_overview(user_id)
    
    return jsonify(overview), 200

# @user_bp.route('/logout')
# def logout():
#     session.clear()
#     flash('Logged Out', 'info')
#     return redirect(url_for('users.login'))

# from form.user_form import RequestResetForm
# @user_bp.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         flash('If an account with that email exists, a password reset link has been sent.', 'info')
#         return redirect(url_for('users.login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)