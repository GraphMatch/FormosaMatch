# manage.py

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app as application
from app import db, graph
from modelssql.question_list import QuestionList
from modelssql.user import User
from modelssql.match import Match
from modelssql.question import Question
from modelssql.match import Match
from modelssql.message import Message
from modelsneo.user import User as UserNeo
import datetime
import csv
import os


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
    user = User(preference = 1, gender = 'woman', birth_date = '1991-01-03', country = 'Taiwan', city = 'Hsinchu City',
    email = 'admin@formosamatch.tw', username = 'admin', password='admin', latitude = 24.8047, longitude = 120.9714)
    db.session.add(user)
    db.session.commit()

@manager.command
def create_match_users():
    user = User(preference = "straight", gender = 'man', birth_date = '1991-01-03', country = 'Taiwan', city = 'Hsinchu City',
    email = 'roblescoulter@gmail.com', username = 'roblescoulter', password='admin123', latitude = 24.8047, longitude = 120.9714)
    db.session.add(user)
    db.session.commit()

    user1 = User(preference = "straight", gender = 'woman', birth_date = '1991-01-03', country = 'Taiwan', city = 'Hsinchu City',
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

@manager.command
def create_photos():
    """Creates the list of profile pictures"""
    with open('crawleddata/photos.csv', 'r', encoding='utf-8', errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        line = 0
        for row in csvreader:
            line += 1
            check_user = User.query.filter_by(username = row[1].strip()).first()
            if(check_user):
                if(check_user.profile_picture is None):
                    check_user.profile_picture = row[0]
            print("User ", line, " photo updated")
        db.session.commit()
    print("Finished")

@manager.command
def create_neo4j_and_rdb_from_csv():
    """
    Creates the neo4j DB initial data and the RDB initial data from the CSV file
    """

    with open('crawleddata/Profiles.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        rowNumber = 0
        for row in csvreader:
            # if rowNumber == 300:
                # break
            if (row[0] != 'birthDateDay'):
                print (rowNumber)
                rowNumber = rowNumber + 1
                birthDateDay = (row[0])
                birthDateMonth = (row[1])
                birthDateYear = (row[2])
                birthDateFull = (birthDateYear+"-"+birthDateMonth+"-"+birthDateDay)
                bodytype = (row[3])
                drinking = (row[4])
                educationValue = (row[5])
                gender = (row[6])
                heightCm = (row[7])
                locationFormatted = (row[8])
                smoking = (row[9])
                username = (row[10])
                email = username+"@gmail.com"
                latitude = float(row[11])
                longitude = float(row[12])
                minAge = (row[13])
                maxAge = (row[14])
                age = (row[15])
                sexPreference = (row[16])
                orientation = (row[17])

                birth_date = datetime.datetime.strptime(birthDateFull, "%Y-%m-%d")
                user = User(orientation, gender, birth_date, 'Taiwan', locationFormatted, email, username, 'admin123',  latitude, longitude, False)
                db.session.add(user)
                db.session.commit()

                user_neo = UserNeo(graph=graph, username=username, latitude=latitude, longitude=longitude,
                    minAge = minAge, maxAge = maxAge, gender = gender, age=user.calculate_age(),
                    orientation = orientation, locationFormatted = locationFormatted,
                    bodyType = bodytype, drinking = drinking,
                    educationValue = educationValue, smoking = smoking, height = heightCm)

                user_neo.register()

    #,,,,,,,,,,,,,,,
    # Loading CSV
    # LOAD CSV WITH HEADERS FROM "file:///crawleddata/Profiles.csv " AS row CREATE (:User { bodyType: (row.bodytype) , drinking:(row.drinking), educationValue: (row.educationValue), gender:(row.gender), height: (row.heightCm), locationFormatted: (row.locationFormatted), orientation: (row.orientation),  smoking: (row.smoking), username: (row.username), latitude: toFloat(row.lat), longitude:toFloat(row.long), minAge: toInt(row.minAge), maxAge: toInt(row.maxAge),  age: toInt(row.age), sexPreference: (row.sexPreference) })
    # queryLoadCsv = "LOAD CSV WITH HEADERS FROM \"file:///crawleddata/Profiles.csv \" AS row CREATE (:User { bodyType: (row.bodytype) , drinking:(row.drinking), educationValue: (row.educationValue), gender:(row.gender), height: (row.heightCm), locationFormatted: (row.locationFormatted), orientation: (row.orientation),  smoking: (row.smoking), username: (row.username), latitude: toFloat(row.lat), longitude:toFloat(row.long), minAge: toInt(row.minAge), maxAge: toInt(row.maxAge),  age: toInt(row.age), sexPreference: (row.sexPreference) })"
    # graph.cypher.execute(queryLoadCsv)

    # Creating index for users
    queryIndexUsers = "CREATE INDEX ON :User(username);"
    graph.cypher.execute(queryIndexUsers)

if __name__ == '__main__':
    manager.run()
