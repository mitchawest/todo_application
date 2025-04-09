from flask import Flask, request
from argparse import ArgumentParser
from modules.todo import Todo
from modules.db import Database
import json
import os

port = os.environ.get('PORT')

parser = ArgumentParser(
    prog="todo_application",
    description="A simple todo list application",
)

parser.add_argument('-p', '--port')
args = parser.parse_args()
port = int(args.port or port or 5000)

db = Database({"db_name": "todo.db"})
db.get_connection()
db.seed()
todos = db.get_todos()

app = Flask(import_name="todo_application")

@app.route("/", methods=["GET"])
def hello():
    return "Welcome to the todo application!"

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Todo):
            return { 'priority': obj.get_priority(), 'name': obj.get_name(), 'is_done': obj.get_is_done() }
        return json.JSONEncoder.default(self, obj)

def get_args():
    is_done = request.args.get("is_done")
    priorities = request.args.get("priority")
    if priorities:
        priorities = priorities.split(",")
    name = request.args.get("name")
    return is_done, priorities, name

@app.route("/foo", methods=["GET"])
def foo():
    return json.dumps({"foo": "bar"})

@app.route("/todos", methods=["GET","POST","DELETE"])
def todos():
    if request.method == "POST":
        db.add_todo(Todo(
            request.json.get("priority"),
            request.json.get("name")
        ))
        return json.dumps(db.get_todos(), cls=CustomEncoder)
    elif request.method == "GET":
        is_done, priorities, name = get_args()
        return json.dumps(db.get_todos(priorities, str(name).lower() if name else None, True if is_done and str(is_done).lower() == "true" else False), cls=CustomEncoder)
    elif request.method == "DELETE":
        _, priorities, _ = get_args()
        print(priorities)
        db.mark_todo_as_done(priorities)
        return json.dumps(db.get_todos(), cls=CustomEncoder)
    else:
        raise NotImplementedError("Method not implemented")

@app.errorhandler(Exception)
def all_exception_handler(error):
   if isinstance(error, ValueError):
       return str(error), 400
   if isinstance(error, NotImplementedError):
       return str(error), 501
   return {"message": str(error), "code": 500}, 500

app.run(host="0.0.0.0", port=port)