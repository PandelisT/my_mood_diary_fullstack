# main.py
from main import db
from flask import  Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User
from forms.forms import RegistrationForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/profile', methods=["POST"])
@login_required
def user_password_change():
    form = RegistrationForm()
    user_id = current_user._get_current_object()
    email = user_id.email
    name = user_id.name
    password = request.form.get('password')
    user_id.password = generate_password_hash(password, method='sha256')
    db.session.commit()
    flash('Password changed')

    return redirect(url_for('main.profile'))
