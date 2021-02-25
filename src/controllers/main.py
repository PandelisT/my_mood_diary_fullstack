from main import db
from flask import Blueprint, render_template, redirect
from flask import url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash


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
    user_id = current_user._get_current_object()
    password = request.form.get('password')
    if len(password) < 6:
        flash('Password not valid')
        return redirect(url_for('main.profile'))
    else:
        user_id.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        flash('Password changed')

    return redirect(url_for('main.profile'))
