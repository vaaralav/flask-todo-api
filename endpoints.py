from models import Todo
from database import db
from auth import auth
from flask import Blueprint, abort, jsonify, request, url_for

api = Blueprint('api', __name__)


# ENDPOINTS
# ----------

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('api.get_task', task_id=task['id'], _external=True)
            new_task['id'] = task['id']
        else:
            new_task[field] = task[field]
    return new_task


@api.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify([make_public_task(todo.as_json()) for todo in Todo.query.all()])

@api.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = Todo(request.json['title'], request.json.get('description', ""), request.json.get('done', False))
    db.session.add(task)
    db.session.flush()
    db.session.commit()

    return jsonify(make_public_task(task.as_json())), 201

@api.route('/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = Todo.query.get(task_id)
    if (task is None):
        abort(404)
    return jsonify(make_public_task(task.as_json()))


@api.route('/tasks/<int:task_id>', methods=['PUT'])
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

@api.route('/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = Todo.query.get(task_id)
    if task is None:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})

@api.route('/health', methods=['GET'])
def get_health():
    return jsonify({'health': 'ok!'})
