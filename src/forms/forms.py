from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, PasswordField, Form
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from models.User import User


class AddJournalEntryForm(FlaskForm):
    journal_entry = TextAreaField([Length(min=1)])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    name = StringField('Name', [Length(min=4, max=25)])
    email = StringField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('New Password', [
        DataRequired(), Length(min=6)
    ])

class AddPsychologistDetails(FlaskForm):
    name = StringField('Name', [Length(min=4, max=25)])
    email = StringField('Email Address', [Length(min=6, max=35)])


