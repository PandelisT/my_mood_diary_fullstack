from main import db
from models.ProblemArea import ProblemArea
from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.User import User
from flask_login import login_user, logout_user, login_required, current_user
from forms.forms import AddProblemAreaEntryForm


problem_area = Blueprint("problem_area", __name__, url_prefix="/problem_area")


@problem_area.route('/new_entry', methods=["GET", "POST"])
@login_required
def problem_area_entry_create():
    form = AddProblemAreaEntryForm()
    if form.validate_on_submit():
        problem_area = ProblemArea()
        problem_area.problem_area_entry = form.problem_area_entry.data
        user_id = current_user._get_current_object()
        problem_area.user_id_fk = user_id.id
        db.session.add(problem_area)
        db.session.commit()

    return redirect(url_for('problem_area.get_problem_area_entries'))

@problem_area.route("/problem_area_entries", methods=["GET"])
@login_required
def get_problem_area_entries():
    user_id = current_user._get_current_object()
    user = user_id.id
    problem_area_entries = ProblemArea.query.filter_by(user_id_fk=user).order_by(ProblemArea.problem_area_date.desc()).all()
    return render_template('problem_area_entries.html', problem_area_entries=problem_area_entries, name=current_user.name)


@problem_area.route("/problem_area_entry/<int:problem_area_id>", methods=["GET"])
@login_required
def get_problem_area_entry(problem_area_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    problem_area_entry = ProblemArea.query.filter_by(user_id_fk=user, id=problem_area_id).first()
    return render_template('problem_area_entry.html', problem_area_entry=problem_area_entry)

@problem_area.route("/problem_area_entries/<int:problem_area_id>", methods=["POST"])
@login_required
def delete_problem_area_entry(problem_area_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    problem_area_entry = ProblemArea.query.filter_by(user_id_fk=user, id=problem_area_id).first()
    db.session.delete(problem_area_entry)
    db.session.commit()
    return redirect(url_for('problem_area.get_problem_area_entries'))


@problem_area.route("/problem_area_entries/update/<int:problem_area_id>", methods=["POST"])
@login_required
def update_problem_area_entry(problem_area_id):
    form = AddProblemAreaEntryForm()
    user_id = current_user._get_current_object()
    user = user_id.id
    update_problem_area_entry = ProblemArea.query.filter_by(user_id_fk=user, id=jproblem_area_id).first()
    update_problem_area_entry.problem_area_entry = form.problem_area_entry.data
    db.session.commit()
    return redirect(url_for('problem_area.get_problem_area_entries'))


@problem_area.route("/problem_area_entry/update/<int:problem_area_id>", methods=["POST"])
@login_required
def update_single_problem_area_entry(problem_area_id):
    form = AddProblemAreaEntryForm()
    user_id = current_user._get_current_object()
    user = user_id.id
    update_problem_area_entry = ProblemArea.query.filter_by(user_id_fk=user, id=problem_area_id).first()
    update_problem_area_entry.problem_area_entry = form.problem_area_entry.data
    db.session.commit()
    return render_template('problem_area_entry.html', problem_area_entry=update_problem_area_entry)
    

