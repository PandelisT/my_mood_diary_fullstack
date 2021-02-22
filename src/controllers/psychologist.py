from main import db
from models.Psychologist import Psychologist
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from forms.forms import AddPsychologistDetails


psychologist = Blueprint("psychologist", __name__, url_prefix="/psychologist")


@psychologist.route('/new_details', methods=["POST"])
@login_required
def post_psychologist_details():
    form = AddPsychologistDetails()
    if form.validate_on_submit():
        psychologist = Psychologist()
        psychologist.name = form.name.data
        psychologist.email = form.email.data
        user_id = current_user._get_current_object()
        psychologist.user_id = user_id.id
        db.session.add(psychologist)
        db.session.commit()

    return render_template('profile.html',
                           psychologist=psychologist,
                           name=current_user.name)


@psychologist.route("/psychologist", methods=["GET"])
@login_required
def get_all_psychologists():
    user_id = current_user._get_current_object()
    user = user_id.id
    psychologists = Psychologist.query.filter_by(user_id=user).all()
    return render_template('profile.html',
                           psychologists=psychologists,
                           name=current_user.name)
