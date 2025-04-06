from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId
from .forms import TodoForm
from application import db
from datetime import datetime


@app.route("/")
def get_todos():
    todos = []
    for todo in db.todos.find().sort("date_created", -1):  # ✅ collection changed to `todos`
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)

    return render_template("view_todos.html", todos=todos)


@app.route("/add_todo", methods=['POST', 'GET'])
def add_todo():
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todos.insert_one({  # ✅ collection changed to `todos`
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        })
        flash("Todo successfully added", "success")
        return redirect("/")
    else:
        form = TodoForm()
    return render_template("add_todo.html", form=form)


@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todos.find_one_and_delete({"_id": ObjectId(id)})  # ✅ collection changed to `todos`
    flash("Todo successfully deleted", "success")
    return redirect("/")


@app.route("/update_todo/<id>", methods=['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todos.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect("/")
    else:
        form = TodoForm()
        todo = db.todos.find_one({"_id": ObjectId(id)})  # ✅ fixed collection name and removed `.find_one_or_404`

        if not todo:
            flash("Todo not found", "danger")
            return redirect("/")

        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed", None)  # ✅ fixed typo

    return render_template("add_todo.html", form=form)
