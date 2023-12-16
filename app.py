"""
    Todo's:
    - create execution parameter
    - parameter setup database key is -sdb and value is [databasename]
"""

from flask import Flask, render_template, request, redirect, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from functools import wraps
from model import *
import re
import datetime

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = "debug>.<q!w@e#r$t%y^"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app, model_class=Base)
Session(app)

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"
GENDERS = ("Male", "Female", "Non-binary")
PASSWORD_ENCRYPT_METHOD = "pbkdf2:sha256"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    if request.method == "POST" and request.content_type == FORM_CONTENT_TYPE:
        """
            Todo's:
            - Prevent form spam 
        """
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        message = request.form.get("message")

        json = {}
        data = {}

        if fullname is None:
            data["fullname"] = "Rejected field!"
        elif fullname == "":
            data["fullname"] = "Missing full name!"
        elif len(fullname) > 60:
            data["fullname"] = "Full name too long!"

        if email is None:
            data["email"] = "Rejected field!"
        elif email == "":
            data["email"] = "Missing email!"
        elif not re.match(EMAIL_REGEX, email):
            data["email"] = "Email address!"

        if message is None:
            data["message"] = "Rejected field!"
        elif message == "":
            data["message"] = "Missing message!"
        elif len(message) > 1024:
            data["message"] = "Message too long!"

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        data = ContactUs(full_name=fullname, email=email, message=message, created_date=datetime.datetime.now())
        db.session.add(data)
        db.session.commit()

        json["status"] = 200
        json["message"] = "Thank you for reaching out! Your message has been successfully received. Our team will review it and get back to you as soon as possible."
        json["data"] = {}
        return jsonify(json)

    else:
        return render_template("contactus.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and request.content_type == FORM_CONTENT_TYPE:
        """
            Todo's:
            - Prevent registration spam
        """
        email = request.form.get("email")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        json = {}
        data = {}

        if email is None:
            data["email"] = "Rejected field!"
        elif email == "":
            data["email"] = "Missing email!"
        elif not re.match(EMAIL_REGEX, email):
            data["email"] = "Email address!"
        elif db.session.execute(select(User).filter_by(email=email)).one_or_none():
            data["email"] = "Uh-oh! This email has already been registered."

        if password is None:
            data["password"] = "Rejected field!"
        elif password == "":
            data["password"] = "Missing password!"
        elif len(password) > 30:
            data["password"] = "Password too long!"

        if repassword is None:
            data["repassword"] = "Rejected field!"
        elif repassword == "":
            data["repassword"] = "Missing confirm password!"
        elif len(repassword) > 30:
            data["repassword"] = "Confirm password too long!"
        elif repassword != password:
            data["repassword"] = "Confirm password not match!"

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        user = User(email=email, password=generate_password_hash(password, PASSWORD_ENCRYPT_METHOD), email_verified=False, is_user_ext=False, registered_date=datetime.datetime.now())
        db.session.add(user)
        db.session.flush()
        userExt = UserExt(user=user.id, first_name="", middle_name="", last_name="", gender="", birth=datetime.date(1899, 12, 31))
        db.session.add(userExt)
        db.session.commit()

        json["status"] = 200
        json["message"] = "You're successfully registered!"
        json["data"] = {}
        return jsonify(json)

    else:
        return render_template("auth/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.content_type == FORM_CONTENT_TYPE:
        """
            Todo's:
            - Add session if user login successfully
            - Prevent login spam
        """
        email = request.form.get("email")
        password = request.form.get("password")

        json = {}
        data = {}

        if email is None:
            data["email"] = "The email or password you entered is incorrect!"
        elif email == "":
            data["email"] = "The email or password you entered is incorrect!"
        elif not re.match(EMAIL_REGEX, email):
            data["email"] = "The email or password you entered is incorrect!"

        if password is None:
            data["email"] = "The email or password you entered is incorrect!"
        elif password == "":
            data["email"] = "The email or password you entered is incorrect!"
        elif len(password) > 30:
            data["email"] = "The email or password you entered is incorrect!"

        result = ()

        if not data:
            result = db.session.execute(select(User).filter_by(email=email)).one_or_none()

            if result is None or not check_password_hash(result[0].password, password):
                data["email"] = "The email or password you entered is incorrect!"

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        session["user_id"] = result[0].id

        json["status"] = 302
        json["message"] = "You're successfully login!"
        json["location"] = "/"

        return jsonify(json)
    else:
        return render_template("auth/login.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    if "user_id" in session:
        session.clear()

    return redirect("/")

def AccountUser(firstname, middlename, lastname, gender, birth):
    data = {}

    if firstname is None:
        data["user"] = "Rejected field!"
    elif firstname == "":
        data["user"] = "Missing first name!"
    elif len(firstname) > 30:
        data["user"] = "First name too long!"

    if middlename is None:
        data["user"] = "Rejected field!"
    elif len(middlename) > 30:
        data["user"] = "Middle name too long!"

    if lastname is None:
        data["user"] = "Rejected field!"
    elif lastname == "":
        data["user"] = "Missing last name!"
    elif len(lastname) > 30:
        data["user"] = "Last name too long!"

    if gender is None:
        data["user"] = "Rejected field!"
    elif gender == "":
        data["user"] = "Missing gender!"
    elif gender not in GENDERS:
        data["user"] = "Provide your gender!"

    if birth is None:
        data["user"] = "Rejected field!"
    else:
        try:
            birth = datetime.date.fromisoformat(birth)
        except ValueError:
            data["user"] = "Rejected field!"

    if not data:
        userext = db.session.execute(select(UserExt).filter_by(user=session["user_id"])).one_or_none()
        userext = userext[0]
        userext.first_name = firstname
        userext.middle_name = middlename
        userext.last_name = lastname
        userext.gender = gender
        userext.birth = birth
        db.session.commit()

    return data

@app.route("/me/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST" and request.content_type == FORM_CONTENT_TYPE:
        action = request.form.get("action")
        try:
            action = int(action)
        except ValueError:
            return redirect("/me/account")

        json = {}
        data = {}

        if action == 0: # User Information
            data = AccountUser(firstname = request.form.get("firstname"),
                        middlename = request.form.get("middlename"),
                        lastname = request.form.get("lastname"),
                        gender = request.form.get("gender"),
                        birth = request.form.get("birth"))

            if not data:
                json["status"] = 200
                json["message"] = "User Information Updated!"
                json["data"] = {}
        elif action == 1: # Email
            email = request.form.get("email")

            if email is None:
                data["email"] = "Rejected field!"
            elif email == "":
                data["email"] = "Missing email!"
            elif not re.match(EMAIL_REGEX, email):
                data["email"] = "Email address!"

            if not data:
                user = db.session.execute(select(User).filter_by(id=session["user_id"])).one_or_none()
                user = user[0]

                if user.email == email:
                    data["email"] = "Uh-oh! This email has not change."
                else:
                    user.email = email
                    db.session.commit()
                    json["status"] = 200
                    json["message"] = "Email Updated!"
                    json["data"] = {}
        elif action == 2: # Password
            password = request.form.get("password")
            newPassword = request.form.get("newpassword")
            newRePassword = request.form.get("newrepassword")

            if password is None:
                data["password"] = "Rejected field!"
            elif password == "":
                data["password"] = "Missing password!"
            elif len(password) > 30:
                data["password"] = "Password too long!"

            if newPassword is None:
                data["password"] = "Rejected field!"
            elif newPassword == "":
                data["password"] = "Missing new password!"
            elif len(newPassword) > 30:
                data["password"] = "New password too long!"

            if newRePassword is None:
                data["password"] = "Rejected field!"
            elif newPassword != newRePassword:
                data["password"] = "Confirm new password not match!"

            if not data:
                user = db.session.execute(select(User).filter_by(id=session["user_id"])).one_or_none()
                user = user[0]

                if not check_password_hash(user.password, password):
                    data["password"] = "Password incorrect!"
                else:
                    newPassword = generate_password_hash(newPassword, PASSWORD_ENCRYPT_METHOD)
                    user.password = newPassword
                    db.session.commit()
                    json["status"] = 200
                    json["message"] = "Password Updated!"
                    json["data"] = {}

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        return jsonify(json)

    else:
        userext = db.session.execute(select(UserExt).filter_by(user=session["user_id"])).one_or_none()
        userext = userext[0]

        return render_template("me/account.html", userext=userext)

@app.route("/me/listing", methods=["GET"])
@login_required
def listing():
    return render_template("/me/listing.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()