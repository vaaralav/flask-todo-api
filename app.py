#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for, g
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(512), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title: str, description: str, done: bool=False):
        self.title = title
        self.description = description
        self.done = done

    def as_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done
        }

db.create_all()

# AUTH
# ----
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
            new_task['id'] = task['id']
        else:
            new_task[field] = task[field]
    return new_task

# ENDPOINTS
# ----------

@app.route('/todo/api/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify([make_public_task(todo.as_json()) for todo in Todo.query.all()])

@app.route('/todo/api/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = Todo(request.json['title'], request.json.get('description', ""), request.json.get('done', False))
    db.session.add(task)
    db.session.flush()
    db.session.commit()

    return jsonify(make_public_task(task.as_json())), 201

@app.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = Todo.query.get(task_id)
    if (task is None):
        abort(404)
    return jsonify(make_public_task(task.as_json()));


@app.route('/todo/api/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = Todo.query.get(task_id)
    if task is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    return jsonify(make_public_task(task.as_json()))

@app.route('/todo/api/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = Todo.query.get(task_id)
    if task is None:
        abort(404)
    db.session.delete(task);
    db.session.commit()
    return jsonify({'result': True})

@app.route('/todo/api/health', methods=['GET'])
def get_health():
    return jsonify({'health': 'ok!'})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)
@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

if __name__ == '__main__':
    app.run(debug=True)
