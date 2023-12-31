"""
    Todo's:
"""

from flask import Flask, render_template, request, redirect, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, join, or_
from functools import wraps
from model import *
from os import getcwd
from os.path import abspath, join
import re
import datetime
import csv
import sys
import argparse

UPLOAD_FOLDER = join(abspath(getcwd()), "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"
GENDERS = ("Male", "Female", "Non-binary")
PASSWORD_ENCRYPT_METHOD = "pbkdf2:sha256"
PASSWORD_LENGTH_ALLOWED = 30

parser = argparse.ArgumentParser(
                    prog="app.py",
                    description="Customer to Customer e-commerce")
parser.add_argument("-skey", type=str, help="If no argument is passed use default. A secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application.")
parser.add_argument("-db", "-db-uri", type=str, required=True, help="The database URI that should be used for the connection. Examples: sqlite:////tmp/test.db, mysql://username:password@server/db")
args = parser.parse_args()

app = Flask(__name__)
app.secret_key = "debug>.<q!w@e#r$t%y^" if not args.skey else args.skey
app.config["SQLALCHEMY_DATABASE_URI"] = args.db #"sqlite:///db.sqlite3"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app, model_class=Base)
Session(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def AllowedImageFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    categories = db.session.execute(select(Category)).fetchall()
    return render_template("index.html", categories=categories)

@app.route("/q", methods=["GET"])
def q():
    products = db.session.execute(select(Product, ProductImage).
                                    where(Product.title.like("%{}%".format(request.args["title"])), Product.is_deleted == False).
                                    group_by(ProductImage.product_id).
                                    join(ProductImage, Product.id == ProductImage.product_id)).fetchall()

    return render_template("search.html", products=products)

@app.route("/product/<int:id>", methods=["GET"])
def product(id):
    if id <= 0:
        return redirect("/")

    product = db.session.execute(select(Product).where(Product.id == id, Product.is_deleted == False)).one_or_none()

    if product is None:
        return redirect("/")

    productImgs = db.session.execute(select(ProductImage).where(ProductImage.product_id == id)).fetchall()
    productCategory = db.session.execute(select(Category).where(Category.id == product[0].category)).one_or_none()
    userExt = db.session.execute(select(UserExt).where(UserExt.user_id == product[0].user_id)).one_or_none()

    return render_template("/product/viewProduct.html", product=product, productImgs=productImgs, productCategory=productCategory, userExt=userExt)

@app.route("/me/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST" and request.content_type == "application/json":
        try:
            userReq = request.get_json()
        except:
            return redirect("/")

        if "action" not in userReq:
            return redirect("/")

        if userReq["action"] == "GetChats":
            results = db.session.execute(select(Chat.id, Chat.product_id, UserExt.first_name, UserExt.middle_name, UserExt.last_name, Product.title).
                                    join(UserExt, Chat.user2_id == UserExt.user_id).
                                    join(Product, Chat.product_id == Product.id).
                                    where(Chat.user1_id == session["user_id"]).
                                    union(select(Chat.id, Chat.product_id, UserExt.first_name, UserExt.middle_name, UserExt.last_name, Product.title).
                                    join(UserExt, Chat.user1_id == UserExt.user_id).
                                    join(Product, Chat.product_id == Product.id).
                                    where(Chat.user2_id == session["user_id"]))).fetchall()

            chats = []
            for result in results:
                chat = {}
                chat["chat_id"] = result.id
                chat["first_name"] = result.first_name
                chat["middle_name"] = result.middle_name
                chat["last_name"] = result.last_name
                chat["subject"] = result.title
                chats.append(chat)

            return jsonify(chats)
        elif userReq["action"] == "GetChatMessages":
            if "chat_id" not in userReq:
                return redirect("/")

            result = db.session.execute(select(Chat.id).
                                    join(UserExt, Chat.user2_id == UserExt.user_id).
                                    where(Chat.user1_id == session["user_id"], Chat.id == userReq["chat_id"]).
                                    union(select(Chat.id).
                                    join(UserExt, Chat.user1_id == UserExt.user_id).
                                    where(Chat.user2_id == session["user_id"], Chat.id == userReq["chat_id"]))).fetchall()

            if result is None:
                return redirect("/")

            results = db.session.execute(select(Message).where(Message.chat_id == result[0][0])).fetchall()

            messages = []
            for msg in results:
                message = {}
                message["message_id"] = msg[0].id
                if msg[0].sender_id == session["user_id"]:
                    message["is_sender"] = True
                else:
                    message["is_sender"] = False
                message["message"] = msg[0].message
                message["time_stamp"] = msg[0].time_stamp
                messages.append(message)

            return jsonify(messages)
        elif userReq["action"] == "UpdateChatMessages":
            if "message_id" not in userReq and "chat_id" not in userReq:
                return redirect("/")

            results = db.session.execute(select(Message).filter(Message.id > userReq["message_id"], Message.chat_id == userReq["chat_id"])).fetchall()

            if results is None:
                return redirect("/")
            elif len(results) <= 0:
                return jsonify({})

            messages = []
            for msg in results:
                message = {}
                message["message_id"] = msg[0].id
                if msg[0].sender_id == session["user_id"]:
                    message["is_sender"] = True
                else:
                    message["is_sender"] = False
                message["message"] = msg[0].message
                message["time_stamp"] = msg[0].time_stamp
                messages.append(message)

            return jsonify(messages)
        elif userReq["action"] == "PostChatMessage":
            if "message" not in userReq and "chat_id" not in userReq and "time_stamp" not in userReq:
                return redirect("/")

            message = Message(chat_id=userReq["chat_id"], sender_id=session["user_id"], message=userReq["message"], time_stamp=datetime.datetime.fromtimestamp(userReq["time_stamp"] / 1e3))
            db.session.add(message)
            db.session.commit()

            return jsonify({ "status" : 200, "message_id": message.id })
        elif userReq["action"] == "ChatProduct":
            if "product_id" not in userReq:
                return redirect("/")

            result = db.session.execute(select(Chat).where(Chat.product_id == userReq["product_id"], or_(Chat.user1_id == session["user_id"], Chat.user2_id == session["user_id"]))).one_or_none()

            if result is not None:
                return redirect("/me/chat")

            product = db.session.execute(select(Product).where(Product.id == userReq["product_id"], Product.is_deleted == False, Product.user_id != session["user_id"])).one_or_none()

            if product is None:
                return redirect("/")

            chat = Chat(user1_id=session["user_id"], user2_id=product[0].user_id, product_id=product[0].id)
            db.session.add(chat)
            db.session.flush()
            msg = Message(chat_id=chat.id, sender_id=session["user_id"], message="Hi, I'm interested", time_stamp=datetime.datetime.now())
            db.session.add(msg)
            db.session.commit()

            return jsonify({ "status": 200, "message": "Message sent!" })
    else:
        return render_template("/me/chat.html")

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
        elif len(fullname) > ContactUs.full_name.type.length:
            data["fullname"] = "Full name too long!"

        if email is None:
            data["email"] = "Rejected field!"
        elif email == "":
            data["email"] = "Missing email!"
        elif len(email) > ContactUs.email.type.length:
            data["email"] = "Email too long!"
        elif not re.match(EMAIL_REGEX, email):
            data["email"] = "Email address!"

        if message is None:
            data["message"] = "Rejected field!"
        elif message == "":
            data["message"] = "Missing message!"
        elif len(message) > ContactUs.message.type.length:
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
        elif len(email) > User.email.type.length:
            data["email"] = "Email too long!"
        elif not re.match(EMAIL_REGEX, email):
            data["email"] = "Email address!"
        elif db.session.execute(select(User).filter_by(email=email)).one_or_none():
            data["email"] = "Uh-oh! This email has already been registered."

        if password is None:
            data["password"] = "Rejected field!"
        elif password == "":
            data["password"] = "Missing password!"
        elif len(password) > PASSWORD_LENGTH_ALLOWED:
            data["password"] = "Password too long!"

        if repassword is None:
            data["repassword"] = "Rejected field!"
        elif repassword == "":
            data["repassword"] = "Missing confirm password!"
        elif len(repassword) > PASSWORD_LENGTH_ALLOWED:
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
        userExt = UserExt(user_id=user.id, first_name="", middle_name="", last_name="", gender="", birth=datetime.date(1899, 12, 31))
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

        if email is None or email == "" or len(email) > User.email.type.length or not re.match(EMAIL_REGEX, email):
            data["email"] = "The email or password you entered is incorrect!"

        if password is None or password == "" or len(password) > PASSWORD_LENGTH_ALLOWED:
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
    elif len(firstname) > UserExt.first_name.type.length:
        data["user"] = "First name too long!"

    if middlename is None:
        data["user"] = "Rejected field!"
    elif len(middlename) > UserExt.middle_name.type.length:
        data["user"] = "Middle name too long!"

    if lastname is None:
        data["user"] = "Rejected field!"
    elif lastname == "":
        data["user"] = "Missing last name!"
    elif len(lastname) > UserExt.last_name.type.length:
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

    user = db.session.execute(select(User).where(User.id == session["user_id"])).one_or_none()
    if not user[0].is_user_ext:
        user[0].is_user_ext = True
        db.session.flush()
    else:
        data["user"] = "Already changed!"

    if not data:
        userext = db.session.execute(select(UserExt).filter_by(user_id=session["user_id"])).one_or_none()
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
            elif len(email) > User.email.type.length:
                data["email"] = "Email too long!"
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
            elif len(password) > PASSWORD_LENGTH_ALLOWED:
                data["password"] = "Password too long!"

            if newPassword is None:
                data["password"] = "Rejected field!"
            elif newPassword == "":
                data["password"] = "Missing new password!"
            elif len(newPassword) > PASSWORD_LENGTH_ALLOWED:
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
        userext = db.session.execute(select(UserExt).filter_by(user_id=session["user_id"])).one_or_none()
        userext = userext[0]

        return render_template("me/account.html", userext=userext)

@app.route("/me/listing", methods=["GET", "POST"])
@login_required
def listing():
    if request.method == "POST":
        json = {}
        data = {}

        user = db.session.execute(select(User).where(User.id==session["user_id"])).one_or_none()
        if not user[0].is_user_ext:
            data["listing"] = "Update your user profile first! On your account"
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        action = request.form.get("action")

        if action == "Add":
            title = request.form.get("title")
            price = request.form.get("price")
            category = request.form.get("category")
            description = request.form.get("description")
            availability = request.form.get("availability")
            files = ()

            if title is None:
                data["listing"] = "Rejected field!"
            elif title == "":
                data["listing"] = "Missing title!"
            elif len(title) > Product.title.type.length:
                data["listing"] = "Title too long!"

            if price is None:
                data["listing"] = "Rejected field!"
            else:
                try:
                    price = Product.price.type.python_type(price)
                except:
                    data["listing"] = "Invalid price!"

                if not data:
                    if price <= 0:
                        data["listing"] = "Invalid price!"

            if category is None:
                data["listing"] = "Rejected field!"
            else:
                category = db.session.execute(select(Category).filter_by(id=category)).one_or_none()

                if category is None:
                    data["listing"] = "Invalid category!"

            if description is None:
                data["listing"] = "Rejected field!"
            elif len(description) <= 0:
                data["listing"] = "Missing description!"

            if availability is None:
                data["listing"] = "Rejected field!"
            else:
                try:
                    availability = int(availability)
                    availability = Product.availability.type.python_type(availability)
                except:
                    data["listing"] = "Invalid availability"

            if "images" not in request.files:
                data["listing"] = "No image selected!"
            elif len(request.files.getlist("images")) > 3:
                    data["listing"] = "Product images limit is 3!"
            else:
                files = request.files.getlist("images")

                for file in files:
                    if file.filename == "":
                        data["listing"] = "No image selected!"
                        break
                    elif not AllowedImageFile(file.filename):
                        data["listing"] = "Invalid file type!"
                        break

            if not data:
                product = Product(user_id=session["user_id"], title=title, price=price, category=category[0].id, description=description, availability=availability, mark_sold=False, is_deleted=False)
                db.session.add(product)
                db.session.flush()
                for file in files:
                    filename = secure_filename(file.filename)
                    filename = str(product.id) + str(datetime.datetime.now().strftime("%y%m%d%H%M%S%f")) + filename

                    file.save(join(join(UPLOAD_FOLDER, "imgs"), filename))
                    db.session.add(ProductImage(product_id=product.id, file_name=filename))
                db.session.commit()

                json["status"] = 200
                json["message"] = "Successfully added!"
                json["data"] = {}
        elif action == "Delete":
            if len(request.form) <= 1:
                data["message"] = "No selected item!"

            if not data:
                for x in request.form.values():
                    if x != "Delete":
                        product = db.session.execute(select(Product).where(Product.id == x)).one_or_none()
                        if product is None:
                            data["message"] = "Invalid product item!"
                            break

                        product[0].is_deleted = True
                        db.session.flush()
                        db.session.commit()

                if not data:
                    json["status"] = 200
                    json["message"] = "Successfully deleted!"
                    json["data"] = {}

        if data:
            json["status"] = 400
            json["message"] = "The server cannot or will not process the request due to something that is perceived to be a client error."
            json["data"] = data
            return jsonify(json)

        return jsonify(json)
    else:
        categories = db.session.execute(select(Category)).fetchall()
        products = db.session.execute(select(Product, ProductImage).
                                        where(Product.user_id == session["user_id"], Product.is_deleted == False).
                                        group_by(ProductImage.product_id).
                                        join(ProductImage, Product.id == ProductImage.product_id)).fetchall()

        return render_template("/me/listing.html", categories=categories, products=products)

@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    with app.app_context():
        try:
            csvfile = open('category.csv', newline='')
            reader = csv.reader(csvfile)
        except:
            print("No such file or directory: 'category.csv'")
            sys.exit()

        for row in reader:
            for column in row:
                db.session.add(Category(name=column, description=""))

        try:
            db.session.commit()
        except:
            print("category.csv already exist in db")
        csvfile.close()

    app.run()