from os import name
from flask import Flask, request, render_template, redirect, url_for
from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_login import LoginManager, login_manager, login_required, current_user, login_user, logout_user, UserMixin

app =Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos_db"
app.config["SECRET_KEY"] = "passkey"
Bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    todos = db.relationship('Todo', lazy=True, backref='user')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)


class Todo(db.Model):
    # __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=True)
    is_done = db.Column(db.Boolean, default=False)


@app.route('/home')
@login_required
def index():
    todos = current_user.todos
    return render_template('index.html', todos=todos)


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def create_todo():
    if request.method == 'POST':
        todo = Todo(title=request.form.get('title'),
                    description=request.form.get('description'), user_id=current_user.id, is_done=False)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('todo_form.html')


@app.route('/todo/<int:id>', methods=['GET'])
@login_required
def get_todo(id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=id).first()
    if not todo:
        return "Not Found Any Item"
    return render_template('todo.html', todo=todo)





@app.route('/todo/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return "Not Found Any Item"
    if request.method == "POST":
        todo.title = request.form.get('title')
        todo.description = request.form.get('description')
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('get_todo', id=id))
    return render_template('todo_form.html', todo=todo)


@app.route('/todo/<int:id>/delete', methods=['GET'])
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return "Not Found Any Item"
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form.get('email')).first()
        if not user or not user.check_password(request.form.get('password')):
            return redirect(url_for('login'))
        user.todos
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/signup', methods=['POST', "GET"])
def signup():
    if request.method == 'POST':
        if request.form.get('password') != request.form.get('confirm_password'):
            return redirect(url_for('signup'))
        user = User(
            email=request.form.get('email'),
            username=request.form.get('username')
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        try:
            db.session.commit()
        except:
            return redirect(url_for('signup'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run('127.0.0.1', '5000', debug=True)
# lab1 
'''
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
    '''