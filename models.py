from database import db

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(512), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title: str, description: str, done: bool = False):
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
