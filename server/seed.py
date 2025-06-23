from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash 
from datetime import datetime, timedelta 


from server.app import create_app
from server.models.__init__ import db
from server.models.user import User
from server.models.guest import Guest
from server.models.episode import Episode
from server.models.appearance import Appearance

def seed_database():
    print("Starting database seeding...")

    app = create_app()
    with app.app_context():
        print("Deleting existing data...")
        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()
        User.query.delete()
        db.session.commit()
        print("Existing data deleted.")

        print("Creating users...")
        user1 = User(
            username="admin_user",
            password_hash=generate_password_hash("admin_password")
        )
        user2 = User(
            username="regular_user",
            password_hash=generate_password_hash("password123")
        )
        db.session.add_all([user1, user2])
        db.session.commit() 
        print("Users created.")

        print("Creating guests...")
        guest1 = Guest(name="Conan O'Brien", occupation="Talk Show Host")
        guest2 = Guest(name="Taylor Swift", occupation="Singer-Songwriter")
        guest3 = Guest(name="Elon Musk", occupation="Entrepreneur")
        db.session.add_all([guest1, guest2, guest3])
        db.session.commit() 
        print("Guests created.")

        print("Creating episodes...")
        episode1 = Episode(date=datetime.utcnow() - timedelta(days=30), number=1001)
        episode2 = Episode(date=datetime.utcnow() - timedelta(days=15), number=1002)
        episode3 = Episode(date=datetime.utcnow() - timedelta(days=5), number=1003)
        db.session.add_all([episode1, episode2, episode3])
        db.session.commit() 
        print("Episodes created.")

      
        print("Creating appearances...")
        appearance1 = Appearance(rating=5, guest=guest1, episode=episode1) 
        appearance2 = Appearance(rating=4, guest=guest2, episode=episode1) 
        appearance3 = Appearance(rating=5, guest=guest1, episode=episode2) 
        appearance4 = Appearance(rating=3, guest=guest3, episode=episode3) 

        db.session.add_all([appearance1, appearance2, appearance3, appearance4])
        db.session.commit() 
        print("Appearances created.")

        print("Database seeding complete!")

if __name__ == '__main__':
    seed_database()