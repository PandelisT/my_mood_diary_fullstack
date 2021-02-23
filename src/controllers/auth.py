from main import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.User import User
from forms.forms import RegistrationForm


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        form = RegistrationForm()
        if form.validate():
            email = request.form.get('email')
            name = request.form.get('name')
            password = request.form.get('password')
            new_user = User(email=email, name=name,
                            password=generate_password_hash(
                                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please Log in below.')
            return redirect(url_for('main.profile'))
    except Exception:
        flash('Email already registered')
        render_template('signup.html', form=form, error=form.errors)

    return render_template('signup.html', form=form, error=form.errors)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    return jsonify(swag)