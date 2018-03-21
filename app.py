#!flask/bin/python
from flask import Flask, jsonify, make_response
from database import db
from endpoints import api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/todo.db'
app.register_blueprint(api, url_prefix="/todo/api")
with app.app_context():
    db.init_app(app)

    db.create_all()

    @app.errorhandler(404)
    def not_found():
        return make_response(jsonify({'error': 'Not Found'}), 404)
    @app.errorhandler(400)
    def invalid_request():
        return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
