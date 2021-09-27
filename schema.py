from flask import request, jsonify
from Task_base import created_by, modified_by, created_at, modified_at, user_id


class Register:
    def __init__(self):
        self.data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["E-mail"],
            "password": request.form["password"],
            "contact_no": request.form["contact_no"]
        }

    def sign_up(self):
        return self.data


class add_new_task:
    def __init__(self):
        self.task = {
            "User_id": user_id(),
            "Title": request.form["Title"],
            "Description": request.form["Description"],
            "Due_date": request.form["Due_date"],
            "created_by": created_by(),
            "created_at": created_at(),
            "modified_by": modified_by(),
            "modified_at": modified_at(),
            "is_deleted": False
        }

    def create_new_task(self):
        return self.task

# JWT authentication,
# DB embedded document
# Flask Blueprint
# Docker build, composer
# Test case
# Logging
