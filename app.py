from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "poiawhefiusiuawe"
debug = DebugToolbarExtension(app)


@app.route("/")
def index():
    """ Homepage redirects to /register """

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """ Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, and last_name.
    Make sure you are using WTForms and that your password input hides the characters 
    that the user is typing! """

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session['user_name'] = user.username

        return redirect('/secret')

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """ Show form when submitted will login user
        Form accepts username/pwd """

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['user_name'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ["Bad name/password"]
    return render_template("login.html", form=form)


@app.route("/secret")
def secret_route():
    """ Hidden page for logged-in users """

    if "user_name" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        return render_template("secret.html")
