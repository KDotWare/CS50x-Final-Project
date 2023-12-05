"""
    Todo's:
    - create execution parameter
    - parameter setup database key is -sdb and value is [databasename]
"""

from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.security import generate_password_hash
import re
import sqlite3
import datetime

app = Flask(__name__)

emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
formContentType = "application/x-www-form-urlencoded"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    if request.method == "POST" and request.content_type == formContentType:
        """
            Todo's:
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
        elif len(fullname) > 50:
            data["fullname"] = "Full name too long!"

        if email is None:
            data["email"] = "Rejected field!"
        elif email == "":
            data["email"] = "Missing email!"
        elif not re.match(emailRegex, email):
            data["email"] = "Rejected email!"

        if message is None:
            data["message"] = "Rejected field!"
        if message == "":
            data["message"] = "Missing message!"
        elif len(message) > 1024:
            data["message"] = "Message too long!"

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        conn = sqlite3.connect("development.db")
        cur = conn.cursor()
        cur.execute("BEGIN")
        data = (fullname, email, message, datetime.datetime.now())
        try:
            cur.execute("INSERT INTO contactus (fullname, email, message, createddate) VALUES (?, ?, ?, ?)", data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            return jsonify(json)

        json["status"] = 200
        json["message"] = "Thank you for reaching out! Your message has been successfully received. Our team will review it and get back to you as soon as possible."
        json["data"] = {}
        return jsonify(json)

    else:
        return render_template("contactus.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and request.content_type == formContentType:
        """
            Todo's:
            - validate if email already exist
        """
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        json = {}
        data = {}

        if firstname is None:
            data["firstname"] = "Rejected field!"
        elif firstname == "":
            data["firstname"] = "Missing first name!"
        elif len(firstname) > 30:
            data["firstname"] = "First name too long!"

        if lastname is None:
            data["lastname"] = "Rejected field!"
        elif lastname == "":
            data["lastname"] = "Missing last name!"
        elif len(lastname) > 30:
            data["lastname"] = "Last name too long!"

        if email is None:
            data["email"] = "Rejected field!"
        elif email == "":
            data["email"] = "Missing email!"
        elif not re.match(emailRegex, email):
            data["email"] = "Invalid email!"

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

        conn = sqlite3.connect("development.db")
        cur = conn.cursor()
        cur.execute("BEGIN")
        data = (firstname, lastname, email, generate_password_hash(password, "pbkdf2:sha256"), datetime.datetime.now())
        try:
            cur.execute("INSERT INTO user (firstname, lastname, email, password, registereddate) VALUES (?, ?, ?, ?, ?)", data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            return jsonify(json)

        json["status"] = 200
        json["message"] = "You're successfully registered!"
        json["data"] = {}
        return jsonify(json)

    else:
        return render_template("auth/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.content_type == formContentType:
        """
            Todo's:
            - validate if email not exist
            - insert to database
        """
        email = request.form.get("email")
        password = request.form.get("password")

        json = {}
        data = {}

        if email is None:
            data["email"] = "Rejected field!"
        elif email == "":
            data["email"] = "Missing email!"
        elif not re.match(emailRegex, email):
            data["email"] = "Invalid email!"

        if password is None:
            data["password"] = "Rejected field!"
        elif password == "":
            data["password"] = "Missing password!"
        elif len(password) > 30:
            data["password"] = "Password too long!"

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        json["status"] = 200
        json["message"] = "You're successfully login!"
        json["data"] = data
        return jsonify(json)
    else:
        return render_template("auth/login.html")

if __name__ == "__main__":
    app.run()