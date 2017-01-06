# manage.py

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app as application
from app import db
from modelssql.question_list import QuestionList
from modelssql.user import User
from modelssql.question import Question
from modelssql.match import Match
from modelssql.message import Message
import datetime
import csv


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
    email = 'admin@formosamatch.tw', username = 'admin', password='admin', confirmed = True, confirmed_on = datetime.datetime.now(), latitude = 24.8047, longitude = 120.9714, admin = True)
    db.session.add(user)
    db.session.commit()

@manager.command
def create_data():
    """Creates sample data."""
    pass

@manager.command
def create_questions():
    """Creates the list of questions"""
    with open('uploads/questions_1.csv', 'r', encoding='utf-8', errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        line = 0
        for row in csvreader:
            line += 1
            array = row[0].split(",")
            question = QuestionList(text = array[0])
            db.session.add(question)
            print("Question ", line, " added")
        db.session.commit()
    print("Finished")


if __name__ == '__main__':
    manager.run()
