from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

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

        session['username'] = user.username

        return redirect(f'/users/{user.username}')

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
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad name/password"]
    return render_template("login.html", form=form)


@app.route("/users/<username>")
def show_user_profile(username):
    """ Hidden page for logged-in users """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif username != session['username']:
        flash("You can only view your profile!")
        return redirect(f'/users/{session["username"]}')

    else:
        user = User.query.get_or_404(username)
        return render_template("profile.html", user=user)


@app.route("/logout")
def logout_user():
    """"Logout user"""

    session.pop("username")
    return redirect("/")


@app.route("/users/<username>/delete", methods=['POST'])
def delete_user_profile(username):
    """ Hidden page for logged-in users """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif username != session['username']:
        flash("You can only delete your profile!")
        return redirect(f'/users/{session["username"]}')

    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

        return redirect("/")


@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback(username):
    """ Hidden page for logged-in users """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif username != session['username']:
        flash("You can only give yourself feedback!")
        return redirect(f'/users/{session["username"]}')

    else:
        user = User.query.get_or_404(username)
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title=title,
                                    content=content,
                                    username=username)

            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f'/users/{session["username"]}')

        return render_template("feedback.html", user=user, form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """ Hidden page for logged-in users """

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif feedback.user.username != session['username']:
        flash("You can only give yourself feedback!")
        return redirect(f'/users/{session["username"]}')

    else:
        user = User.query.get_or_404(feedback.user.username)
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.commit()

            return redirect(f'/users/{session["username"]}')

        return render_template("edit-feedback.html", user=user, feedback=feedback, form=form)


@app.route("/feedback/<int:feedback_id>/delete", methods=['POST'])
def delete_feedback(feedback_id):
    """ Hidden page for logged-in users """

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif feedback.user.username != session['username']:
        flash("You can only give yourself feedback!")
        return redirect(f'/users/{session["username"]}')

    else:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{session["username"]}')
