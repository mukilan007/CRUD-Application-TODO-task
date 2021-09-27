from functools import wraps
from json import dumps

from flask import Response, request, session

import user
from schema import add_new_task
from user import app, db
from bson.objectid import ObjectId
from Task_base import modified_by, modified_at


@user.login_required
def create_task():
    db.task.insert_one(add_new_task().create_new_task())
    return "Task created"


@user.login_required
def update_task(id):
    respond = db.task.update_many(
        {"_id": ObjectId(id), "User_id": session["id"]},
        {"$set": {"Title": request.form["Title"], "Description": request.form["Description"],
                  "Due_date": request.form["Due_date"], "is_completed": bool(request.form["is_completed"])}})
    if respond.modified_count >= 1:
        db.task.update_many(
            {"_id": ObjectId(id)},
            {"$set": {"modified_by": modified_by(), "modified_at": modified_at()}})
        return "Task changed"
    return "nothing to update"


@user.login_required
def delete_task(id):
    respond = db.task.update_one({"_id": ObjectId(id), "User_id": session["id"]}, {"$set": {"is_deleted": True}})
    if respond.modified_count >= 1:
        return "task deleted"
    return "cannot find the task"



@user.login_required
def find_task(id):
    try:
        detail = list(db.task.find({"_id": ObjectId(id), "User_id": session["id"], "is_deleted": False}))
        for i in detail:
            i["_id"] = str(i["_id"])
            i["created_at"] = str(i["created_at"])
            i["modified_at"] = str(i["modified_at"])
        return Response(response=dumps(detail),
                        status=200,
                        mimetype="application/json")
    except Exception:
        return "cannot find a task"


@user.login_required
def task_list():
    get_task = list(db.task.find({"User_id": session["id"], "is_deleted": False}))
    for i in get_task:
        i["_id"] = str(i["_id"])
        i["created_at"] = str(i["created_at"])
        i["modified_at"] = str(i["modified_at"])
    return Response(response=dumps(get_task),
                    status=200,
                    mimetype="application/json")


app.add_url_rule(rule="/create/task", endpoint="create task", view_func=create_task, methods=["POST"])
app.add_url_rule(rule="/update/task/<id>", endpoint="update task", view_func=update_task, methods=["PATCH"])
app.add_url_rule(rule="/delete/task/<id>", endpoint="delete task", view_func=delete_task, methods=["DELETE"])
app.add_url_rule(rule="/find/task/<id>", endpoint="find task", view_func=find_task, methods=["GET"])
app.add_url_rule(rule="/task/list/", view_func=task_list, methods=["GET"])
