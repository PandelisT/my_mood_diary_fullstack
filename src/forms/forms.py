from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


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


class AddSkillEntryForm(FlaskForm):
    skill_entry = TextAreaField([Length(min=1)])
    submit = SubmitField('Submit')


class AddProblemAreaEntryForm(FlaskForm):
    problem_area_entry = TextAreaField([Length(min=1)])
    submit = SubmitField('Submit')
