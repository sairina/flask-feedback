from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class RegisterUserForm(FlaskForm):
    """ Form for registering user """

    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired(),
                             EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Repeat Password")
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    is_admin = BooleanField("Admin")
    submit_button = SubmitField("Add New User")


class LoginUserForm(FlaskForm):
    """ Form for logging in user """

    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit_button = SubmitField("Login")


class FeedbackForm(FlaskForm):
    """"Form for giving yourself feedback"""

    title = StringField("Title", validators=[Length(min=1, max=100),
                                             InputRequired()])
    content = TextField("Feedback", validators=[InputRequired()])
    submit_button = SubmitField("Submit")
