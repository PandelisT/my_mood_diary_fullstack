from main import db
from models.Psychologist import Psychologist
from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.User import User
from flask_login import login_user, logout_user, login_required, current_user
from forms.forms import AddPsychologistDetails


psychologist = Blueprint("psychologist", __name__, url_prefix="/psychologist")


@psychologist.route('/new_details', methods= ["POST"])
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

    return redirect(url_for('main.profile'))

@psychologist.route("/<int:psychologist_id>", methods=["GET"])
@login_required
def get_psychologist(psychologist_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    psychologist = Psychologist.query.filter_by(user_id_fk=user, id=psychologist_id).first()
    return redirect(url_for('main.profile', psychologist=psychologist)) 

# @journal.route("/journal_entries/<int:journal_id>", methods=["POST"])
# @login_required
# def delete_journal_entry(journal_id):
#     user_id = current_user._get_current_object()
#     user = user_id.id
#     journal_entry = Journal.query.filter_by(user_id_fk=user, id=journal_id).first()
#     db.session.delete(journal_entry)
#     db.session.commit()
#     return redirect(url_for('journal.get_journal_entries'))