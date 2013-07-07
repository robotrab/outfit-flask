from outfit import app
from outfit.models import user, post
from outfit import config
from flask import Flask, session, redirect, url_for, escape, request, render_template
import pymongo
import re

connection = pymongo.MongoClient(config.c['DB_URL'])
database = connection[config.c['DB']]

users = user.User(database)
posts = post.Post(database)
app.secret_key = config.c['SECRET']

###############################################################
#INDEX AND PROFILE
###############################################################

@app.route('/')
def index():
    username = None
    if 'username' in session:
        username = session['username']
        return profile_home(username)

    return render_template("index.html", username=username)

def profile_home(username):
    user_info = users.get_user(username)
    post_info = posts.get_all_posts(username)
    return render_template("profile_home.html", user_info=user_info, post_info=post_info)

###############################################################
#AUTHENTICATION AND SIGNUP
###############################################################

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return post_signup(request)
    else:
        return render_template("signup.html")

def post_signup(request):
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    verify = request.form["verify"]

    # set these up in case we have an error case
    errors = {'username': username, 'email': email}
    if validate_signup(username, password, verify, email, errors):
        if not users.add_user(username, password, email):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return render_template("signup.html", errors=errors)

        session['username'] = request.form['username']
        return redirect(url_for("welcome"))
    else:
        print "user did not validate"
        return render_template("signup.html", errors=errors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return post_login(request)
    else:
        return render_template("login.html")

def post_login(request):
    username = request.form["username"]
    password = request.form["password"]

    user_record = users.validate_login(username, password)
    if user_record:
        # username is stored in the user collection in the _id key
        session['username'] = user_record['_id']

        # if session_id is None:
        #     bottle.redirect("/internal_error")

        return redirect(url_for("welcome"))

    else:
        return render_template("login.html", username=username, password="", login_error="Invalid Login")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template("welcome.html", username=session['username'])
    return redirect(url_for("signup"))


# Helper Functions

# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, verify, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False

    if password != verify:
        errors['verify_error'] = "password must match"
        return False

    if not EMAIL_RE.match(email):
        errors['email_error'] = "invalid email address"
        return False

    return True
