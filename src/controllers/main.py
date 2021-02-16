# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# @psychologist.route('psychologist/new_details', methods= ["POST"])
# @login_required
# def post_psychologist_details():
#     form = AddPsychologistDetails()
#     if form.validate_on_submit():
#         psychologist = Psychologist()
#         psychologist.name = form.name.data
#         psychologist.email = form.email.data
#         user_id = current_user._get_current_object()
#         psychologist.user_id = user_id.id
#         db.session.add(psychologist)
#         db.session.commit()

#     return redirect(url_for('main.profile'))

# @psychologist.route("psychologist//<int:psychologist_id>", methods=["GET"])
# @login_required
# def get_psychologist(psychologist_id):
#     user_id = current_user._get_current_object()
#     user = user_id.id
#     psychologist = Psychologist.query.filter_by(user_id_fk=user, id=psychologist_id).first()
#     return redirect(url_for('main.profile', psychologist=psychologist)) 