from database import db

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(512), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title: str, description: str, user_id: int, done: bool = False):
        self.title = title
        self.description = description
        self.done = done
        self.user = user_id

    def as_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "user": self.user
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), index = True)

    def __init__(self, name: str):
        self.name = name

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
