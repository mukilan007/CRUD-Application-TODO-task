from flask import session, jsonify
import datetime

def admin():
    a = dict()
    for i in session['user']:
        a['user_id'] = i['_id']
        a['Name'] = i['first_name']
        a['email id'] = i['email']
    return a

def created_by():
    return admin()


def created_at():
    return datetime.datetime.now()


def modified_by():
    return admin()


def modified_at():
    return datetime.datetime.now()


def user_id():
    a = admin()
    return a['user_id']
