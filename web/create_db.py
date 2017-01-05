# manage.py

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app as application
from app import db
from modelssql.question_list import QuestionList
from modelssql.user import User
from modelssql.match import Match
from modelssql.question import Question
from modelssql.match import Match
from modelssql.message import Message
import datetime


migrate = Migrate(application, db)
manager = Manager(application)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    user = User(preference = 1, gender = 'F', birth_date = '1991-01-03', country = 'Taiwan', city = 'Hsinchu City',
    email = 'admin@formosamatch.tw', username = 'admin', password='admin', latitude = 24.8047, longitude = 120.9714)
    db.session.add(user)
    db.session.commit()
    # user.create_user_node()

@manager.command
def create_match_users():
    user = User(preference = "straight", gender = 'M', birth_date = '1991-01-03', country = 'Taiwan', city = 'Hsinchu City',
    email = 'roblescoulter@gmail.com', username = 'roblescoulter', password='admin123', latitude = 24.8047, longitude = 120.9714)
    db.session.add(user)

    user1 = User(preference = "straight", gender = 'F', birth_date = '1991-01-03', country = 'Taiwan', city = 'Hsinchu City',
    email = 'alemeraz@gmail.com', username = 'alemeraz', password='admin123', latitude = 24.8047, longitude = 120.9714)
    db.session.add(user1)
    db.session.commit()

    match = Match(True, user.id, user1.id)
    db.session.add(match)
    db.session.commit()

    message1 = Message("Hello you!", match.id, user.id)
    db.session.add(message1)

    message2 = Message("Nihao! How are you Luis?", match.id, user1.id)
    db.session.add(message1)

    db.session.commit()


@manager.command
def create_data():
    """Creates sample data."""
    pass


if __name__ == '__main__':
    manager.run()
