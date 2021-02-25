from main import db
from models.Journal import Journal
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from forms.forms import AddJournalEntryForm
from datetime import datetime
from sqlalchemy import func


journal = Blueprint("journal", __name__, url_prefix="/journal")


@journal.route('/new_entry', methods=["GET", "POST"])
@login_required
def journal_entry_create():
    form = AddJournalEntryForm()
    if form.validate_on_submit():
        journal = Journal()
        journal.journal_entry = form.journal_entry.data
        user_id = current_user._get_current_object()
        journal.user_id_fk = user_id.id
        db.session.add(journal)
        db.session.commit()

    return redirect(url_for('journal.get_journal_entries'))


@journal.route("/journal-entries", methods=["GET"])
@login_required
def get_journal_entries():
    user_id = current_user._get_current_object()
    user = user_id.id
    journal_entries = Journal.query.filter_by(
        user_id_fk=user).order_by(Journal.journal_date.desc()).all()
    return render_template('journal_entries.html',
                           journal_entries=journal_entries,
                           name=current_user.name)


@journal.route("/journal-entry/<int:journal_id>", methods=["GET"])
@login_required
def get_journal_entry(journal_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    journal_entry = Journal.query.filter_by(user_id_fk=user,
                                            id=journal_id).first()
    return render_template('journal_entry.html', journal_entry=journal_entry)


@journal.route('/query', methods=['GET'])
def query_journal():
    try:
        user_id = current_user._get_current_object()
        user = user_id.id
        entry = request.args.get('entry')
        datetime_object = datetime.strptime(entry, "%Y-%m-%d")
        journal_entries = db.session.query(Journal).filter(
            func.date(Journal.journal_date) == datetime_object).filter(
                Journal.user_id_fk == user).all()

        return render_template('journal_entries.html',
                               journal_entries=journal_entries,
                               name=current_user.name)
    except (Exception):
        return render_template('journal_entries.html')


@journal.route("/journal-entries/<int:journal_id>", methods=["POST"])
@login_required
def delete_journal_entry(journal_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    journal_entry = Journal.query.filter_by(user_id_fk=user,
                                            id=journal_id).first()
    db.session.delete(journal_entry)
    db.session.commit()
    return redirect(url_for('journal.get_journal_entries'))


@journal.route("/journal-entry/update/<int:journal_id>", methods=["POST"])
@login_required
def update_single_journal_entry(journal_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    update_journal_entry = Journal.query.filter_by(user_id_fk=user,
                                                   id=journal_id).first()
    update_journal_entry.journal_entry = request.form.get("journal_entry")
    db.session.commit()
    return render_template('journal_entry.html',
                           journal_entry=update_journal_entry)
