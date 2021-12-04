from os import name
from flask import Flask, request, render_template, redirect, url_for

app =Flask(__name__)

todos = []
def get_id():
    id = 1
    if len(todos) > 0:
        id = todos[-1]['id'] +1
    return id 
# @app.route("/greet")
# def greet():
#     return "hello, " + request.args.get("name") if request.args.get("name") is not None else "hello there"

@app.route("/")
def index():

    return render_template("index.html", todos=todos )


@app.route("/todo", methods = ["GET", "POST"]) 
def create_todo():
    if request.method == "POST":
        
       
        todos.append({
            "id": get_id(),
            "title":request.form.get('title'), 
            "description":request.form.get('description'), 
            
        })
        return redirect(url_for('index'))
    return render_template("todo_form.html")

@app.route("/todo/<int:id>", methods = ["GET"]) 
def get_todo(id):
    todo = list( filter(lambda todo: todo["id"] == id, todos))
    if not todo:
        return render_template("not-found.html")
    return render_template("todo.html", todo = todo[0])


@app.route("/todo/<int:id>/edit", methods = ["GET","POST"]) 
def edit_todo(id):
    todo = list( filter(lambda todo: todo["id"] == id, todos))
    if not todo:
        return render_template("not-found.html")
    if request.method == "POST":
        todo[0]['title'] = request.form.get('title')
        todo[0]['description'] = request.form.get('description')
        return redirect(url_for('get_todo', id=id ))
    return render_template("todo_form.html", todo = todo[0])

if __name__ == '__main__':
    app.run("127.0.0.1","8000",debug=True)