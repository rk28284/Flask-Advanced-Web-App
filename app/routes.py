from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
from app.forms import UpdateProfileForm  # Add the form for profile picture upload
from app.models import User
from app.users.utils import save_picture

from flask import jsonify, request
from app.models import User, ProfilePic

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.profile_pic = picture_file
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    profile_pic = url_for('static', filename='uploads/profile_pics/' + user.profile_pic)
    return render_template('profile.html', title='Profile', user=user, profile_pic=profile_pic, form=form)

def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.profile_pic = picture_file
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    profile_pic = url_for('static', filename='uploads/profile_pics/' + user.profile_pic)
    return render_template('profile.html', title='Profile', user=user, profile_pic=profile_pic, form=form)







# Create a new user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Get a list of all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify({"users": user_list})

# Get user details by ID
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})

# Update user details by ID
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data["username"]
    user.email = data["email"]
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Delete user by ID
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# ... Add similar routes for other resources (e.g., profile_pics)
