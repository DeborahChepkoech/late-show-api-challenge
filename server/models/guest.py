from server.models.__init__ import db, SerializerMixin, association_proxy

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=True)


    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    episodes = association_proxy('appearances', 'episode')

    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.name}>'