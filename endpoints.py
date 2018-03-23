from models import Todo, User
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
        elif field == 'user':
            new_task['user_uri'] = url_for('api.get_user', user_id=task['user'], _external = True)
            new_task['user'] = task['user']
        else:
            new_task[field] = task[field]
    return new_task

def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('api.get_user', user_id=user['id'], _external=True)
            new_user['id'] = user['id']
        else:
            new_user[field] = user[field]
    return new_user


@api.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    queries = []
    done = request.args.get('done')
    if done is not None:
        queries.append(Todo.done == done)
    return jsonify([make_public_task(todo.as_json()) for todo in Todo.query.filter(*queries)])

@api.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json or not 'user' in request.json:
        abort(400)
    user = User.query.get(request.json.get('user'))
    if not user:
        abort(404)
    task = Todo(request.json['title'], request.json.get('description', ""),  user.id, request.json.get('done', False))
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

@api.route('/users', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or type(request.json['name']) is not str:
        abort(400)
    new_user = User(request.json['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(make_public_user(new_user.as_json()))

@api.route('/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    return jsonify(make_public_user(user.as_json()))

@api.route('/users/<int:user_id>/tasks', methods=['GET'])
@auth.login_required
def get_user_tasks(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    tasks = Todo.query.filter(Todo.user == user_id)
    return jsonify([make_public_task(task.as_json()) for task in tasks])

@api.route('/health', methods=['GET'])
def get_health():
    return jsonify({'health': 'ok!'})
