from server.models.__init__ import db, SerializerMixin, association_proxy, datetime

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    number = db.Column(db.Integer, unique=True, nullable=False)


    appearances = db.relationship(
        'Appearance',
        back_populates='episode',
        cascade='all, delete-orphan'
    )
    guests = association_proxy('appearances', 'guest')

    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.number} on {self.date.strftime("%Y-%m-%d")}>'