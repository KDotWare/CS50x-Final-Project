from flask import Flask, render_template, request, redirect
import re

app = Flask(__name__)

emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
formContentType = "application/x-www-form-urlencoded"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        message = request.form.get("message")

        if fullname == "" or email == "" or message == "":
            return redirect("/contactus")

        if len(fullname) > 50:
            return redirect("/contactus")

        if not re.match(emailRegex, email):
            return redirect("/contactus")

        if len(message) > 1024:
            return redirect("/contactus")

        #Insert to db here

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

if __name__ == "__main__":
    app.run()