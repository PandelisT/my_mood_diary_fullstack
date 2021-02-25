from main import db
from models.Skill import Skill
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from forms.forms import AddSkillEntryForm


skill = Blueprint("skill", __name__, url_prefix="/skill")


@skill.route('/new_entry', methods=["GET", "POST"])
@login_required
def skill_entry_create():
    form = AddSkillEntryForm()
    if form.validate_on_submit():
        skill = Skill()
        skill.skill_entry = form.skill_entry.data
        user_id = current_user._get_current_object()
        skill.user_id_fk = user_id.id
        db.session.add(skill)
        db.session.commit()

    return redirect(url_for('skill.get_skill_entries'))


@skill.route("/skill_entries", methods=["GET"])
@login_required
def get_skill_entries():
    user_id = current_user._get_current_object()
    user = user_id.id
    skill_entries = Skill.query.filter_by(
        user_id_fk=user).order_by(Skill.skill_date.desc()).all()
    return render_template('skill_entries.html',
                           skill_entries=skill_entries,
                           name=current_user.name)


@skill.route("/skill_entry/<int:skill_id>", methods=["GET"])
@login_required
def get_skill_entry(skill_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    skill_entry = Skill.query.filter_by(user_id_fk=user,
                                        id=skill_id).first()
    return render_template('skill_entry.html',
                           skill_entry=skill_entry)


@skill.route("/skill_entries/<int:skill_id>", methods=["POST"])
@login_required
def delete_skill_entry(skill_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    skill_entry = Skill.query.filter_by(user_id_fk=user,
                                        id=skill_id).first()
    db.session.delete(skill_entry)
    db.session.commit()
    return redirect(url_for('skill.get_skill_entries'))


@skill.route("/skill_entry/update/<int:skill_id>", methods=["POST"])
@login_required
def update_single_skill_entry(skill_id):
    form = AddSkillEntryForm()
    user_id = current_user._get_current_object()
    user = user_id.id
    update_skill_entry = Skill.query.filter_by(
        user_id_fk=user, id=skill_id).first()
    update_skill_entry.skill_entry = form.skill_entry.data
    db.session.commit()
    return render_template('skill_entry.html',
                           skill_entry=update_skill_entry)
