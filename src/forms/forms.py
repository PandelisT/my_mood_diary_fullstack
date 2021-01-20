from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from models.User import User


class AddJournalEntryForm(FlaskForm):
    journal_entry = TextAreaField('Add your journal entry here')
    submit = SubmitField('Submit')
