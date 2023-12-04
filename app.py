from flask import Flask, render_template, request, redirect, jsonify
import re

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
            - add validation for nonetype object from form
            - insert to database
        """
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        message = request.form.get("message")

        json = {}
        data = {}

        if fullname == "":
            data["fullname"] = "Missing full name!"
        elif len(fullname) > 50:
            data["fullname"] = "Full name too long!"

        if email == "":
            data["email"] = "Missing email!"
        elif not re.match(emailRegex, email):
            data["email"] = "Rejected email!"

        if message == "":
            data["message"] = "Missing message!"
        elif len(message) > 1024:
            data["message"] = "Message too long!"

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        json["status"] = 200
        json["message"] = "Thank you for reaching out! Your message has been successfully received. Our team will review it and get back to you as soon as possible."
        json["data"] = data
        return jsonify(json)

    else:
        return render_template("contactus.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and request.content_type == formContentType:
        """
            Todo's:
            - add validation for nonetype object from form
            - validate if email already exist
            - insert to database
        """
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        json = {}
        data = {}

        if firstname == "":
            data["firstname"] = "Missing first name!"
        elif len(firstname) > 30:
            data["firstname"] = "First name too long!"

        if lastname == "":
            data["lastname"] = "Missing last name!"
        elif len(lastname) > 30:
            data["lastname"] = "Last name too long!"

        if email == "":
            data["email"] = "Missing email!"
        elif not re.match(emailRegex, email):
            data["email"] = "Invalid email!"

        if password == "":
            data["password"] = "Missing password!"
        elif len(password) > 30:
            data["password"] = "Password too long!"

        if repassword == "":
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

        json["status"] = 200
        json["message"] = "You're successfully registered!"
        json["data"] = data
        return jsonify(json)

    else:
        return render_template("auth/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.content_type == formContentType:
        """
            Todo's:
            - add validation for nonetype object from form
            - validate if email not exist
            - insert to database
        """
        email = request.form.get("email")
        password = request.form.get("password")

        json = {}
        data = {}

        if email == "":
            data["email"] = "Missing email!"
        elif not re.match(emailRegex, email):
            data["email"] = "Invalid email!"

        if password == "":
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