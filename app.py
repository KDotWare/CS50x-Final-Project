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
            data["fullname"] = "Full name too large!"

        if email == "":
            data["email"] = "Missing email!"
        elif not re.match(emailRegex, email):
            data["email"] = "Invalid email!"

        if message == "":
            data["message"] = "Missing message!"
        elif len(message) > 1024:
            data["message"] = "Message too large!"

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
            - get form values
            - validate form values
            - insert to database
            - create response when success or not
        """
    else:
        return render_template("auth/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.content_type == formContentType:
        """
            Todo's:
            - get form values
            - validate form values
            - insert to database
            - create response when success or not
        """
    else:
        return render_template("auth/login.html")

if __name__ == "__main__":
    app.run()