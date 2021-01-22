from models.Journal import Journal
from main import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.User import User
from flask_login import login_user, logout_user, login_required, current_user
from forms.forms import AddJournalEntryForm


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

    return render_template('journal.html', form=form)

@journal.route("/journal_entries", methods=["GET"])
@login_required
def get_journal_entries():
    user_id = current_user._get_current_object()
    user = user_id.id
    journal_entries = Journal.query.filter_by(user_id_fk=user).all()
    return render_template('journal_entries.html', journal_entries=journal_entries, name=current_user.name)


@journal.route("/journal_entries/<int:journal_id>", methods=["POST"])
@login_required
def delete_journal_entry(journal_id):
    user_id = current_user._get_current_object()
    user = user_id.id
    print(user)
    journal_entry = Journal.query.filter_by(user_id_fk=user, id=journal_id).first()
    print(journal_entry)
    db.session.delete(journal_entry)
    db.session.commit()
    return redirect(url_for('journal.get_journal_entries'))