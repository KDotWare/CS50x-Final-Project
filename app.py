from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contactus", methods=["GET"])
def contactus():
    return render_template("contactus.html")

@app.route("/register", methods=["GET"])
def register():
    return render_template("auth/register.html")

if __name__ == "__main__":
    app.run()