from server.models.__init__ import db, SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    serialize_rules = ('-password_hash',)
    def __repr__(self):
        return f'<User {self.username}>'