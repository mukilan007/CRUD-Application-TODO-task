from functools import wraps

import schema

from json import dumps

from bson.objectid import ObjectId

from flask import Response, request, jsonify, Flask, session, g
from pymongo import MongoClient
from cryptography.fernet import Fernet
from flask_httpauth import HTTPDigestAuth
from passlib.hash import pbkdf2_sha256

client = MongoClient("mongodb+srv://mukilan:1234@cluster0.ug3s6.mongodb.net/crud?retryWrites=true&w=majority")
db = client.crud

app = Flask(__name__)
auth = HTTPDigestAuth()

key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
fernet = Fernet(key)

app.secret_key = b':\xd49\x15\x17\n\xc0\x07\xa9]\xd7\xb2\x93\xa73\xb6'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "you need to login"})
    return wrap


def register():
    respond \
        = schema.Register().sign_up()
    if db.users.find_one({"email": respond['email']}):
        return jsonify({"error": "Email address already exist"}), 400
    respond['password'] = fernet.encrypt(respond["password"].encode())
    db.users.insert_one(respond)
    return Response(response=dumps({"message": "Account created successfully"}),
                    status=200,
                    mimetype="application/json")


def log_in():
    user_email = request.form["email"]
    db_email = list(db.users.find({"email": f"{user_email}"}))
    value = None
    user_password = request.form["password"]
    db_password = None
    for i in db_email:
        value = i["email"]
        db_password = fernet.decrypt(i["password"]).decode()
        i["_id"] = str(i["_id"])
    if user_email == value and user_password == db_password:
        session['user'] = db_email
        for i in db_email:
            session['id'] = i["_id"]
        return "Log in successful!"
    return "Incorrect email id or password, Try Again... "


@login_required
def get_profile():
    try:
        detail = list(db.users.find({"_id": ObjectId(session['id'])}))
        for i in detail:
            i["_id"] = str(i["_id"])
            del i['password']
        return Response(response=dumps(detail),
                        status=200,
                        mimetype="application/json")
    except Exception:
        return "cannot find your profile"


@login_required
def update():
    respond = db.users.update_many(
        {"_id": ObjectId(session['id'])},
        {"$set": {"first_name": request.form["name"], "last_name": request.form["last_name"],
                  "contact_no": request.form["contact_no"]}})
    if respond.modified_count >= 1:
        return "Updated"
    return "cannot update"


@login_required
def delete():
    try:
        # if Task.delete_user_task(id):
        id = session['id']
        db.users.delete_one({"_id": ObjectId(id)})
        session.clear()
        return dumps(f"Account deleted   {id}")
        # return dumps("sorry account not deleted")
    except Exception:
        return dumps("cannot find the account")


@login_required
def log_out():
    session.clear()
    return "Log out successful"


app.add_url_rule(rule="/register", endpoint="register", view_func=register, methods=["POST"])
app.add_url_rule(rule="/users/login", endpoint="login", view_func=log_in, methods=["GET"])
app.add_url_rule(rule="/users/update/", endpoint="update", view_func=update, methods=["PATCH"])
app.add_url_rule(rule="/users/profile/", endpoint="profile", view_func=get_profile, methods=["GET"])
app.add_url_rule(rule="/users/delete/", endpoint="delete", view_func=delete, methods=["DELETE"])
app.add_url_rule(rule="/users/log_out", endpoint="log_out", view_func=log_out, methods=["GET"])
