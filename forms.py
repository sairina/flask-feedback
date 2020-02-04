from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo


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


class LoginUserForm(FlaskForm):
    """ Form for logging in user """

    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
