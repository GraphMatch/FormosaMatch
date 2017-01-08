# app.py

"""#!/usr/bin/env python"""
""" application file """
from flask import Flask
from flask import request, redirect, session, abort, url_for, render_template, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from py2neo import Graph
from config import BaseConfig
import datetime, re, geocoder
from modelssql.utils import *
import sys, traceback
from datetime import date
from werkzeug import secure_filename
import uuid
import os
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import random

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config['DEBUG'] = True
app.config['MAIL_DEBUG'] = True
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAhlmJxd2tyBQGsAdekX8DyQLzGEc09OPA"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

graph = Graph('http://neo4j:admin123@neo4j:7474/db/data/')
# graph = Graph(host='192.168.99.100', http_port=7474, https_port= 7473, bolt_port=7687, user='neo4j', password='admin123')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)
GoogleMaps(app)

from modelssql.user import User
from modelsneo.user import User as UserNeo
from modelssql.match import Match
from modelssql.message import Message
from sqlalchemy.sql import text
from modelssql.question import Question


@app.route('/', methods=['GET', 'POST'])
def index():
    """ index handler """
    if(is_authenticated(session)):
        return redirect(url_for('dashboard'))
    """
        Try to get the country and city from the user IP address
    """
    ip = request.remote_addr
    g = geocoder.ip(ip)
    return render_template('index.html',
    city = g.city,
    country = g.country)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """ dashboard """
    if(not is_authenticated(session)):
        flash('Sorry! You need to log in order to access to this page!')
        return redirect(url_for('index'))
    session_username = session["username"]
    user = User.query.filter_by(username = session_username).first()
    userNeo = UserNeo(graph=graph, username= session_username)
    matches = []
    matchesPictures = {}
    looking_for = "man"#man/woman/everyone
    age_min = 18
    age_max = 29

    interested_in = user.gender #man/woman
    userN = userNeo.find()
    if userN is not None:
        looking_for = (userN['sexPreference'])
        matches = userNeo.get_browse_nodes()
        if userN['minAge'] != None:
            age_min = int(float(userN['minAge']))
        else:
            age_min = userN["age"] - 5
            if age_min < 18:
                age_min = 18
        if userN['maxAge'] != None:
            age_max = int(float(userN['maxAge']))
        else:
            age_max = userN['age'] + 5

        matchesUsernames = []
        for node in matches:
            matchesUsernames.append(node["username"])
        matchesPictures = get_profile_pictures(matchesUsernames)
    return render_template('dashboard.html', current_user = user,
     browse_nodes = matches, nodes_pictures = matchesPictures,
     interested_in = interested_in, looking_for = looking_for, age_min = age_min,
     age_max = age_max )


@app.route('/register', methods=['POST'])
def register():
    orientation = request.form['orientation']
    gender = request.form['gender']
    birth_date_submit = request.form['birth_date']
    country = request.form['country']
    city = request.form['city']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    error = False

    try:
    # if request.method == 'POST':
        """
            Check if the user filled the birthdate
        """
        if(len(birth_date_submit) == 0):
            error = True
            flash('Sorry! You need to provide your birthdate')
            return redirect(url_for('index'))

        birth_date = datetime.datetime.strptime(birth_date_submit, "%Y-%m-%d")
        user = User(orientation, gender, birth_date, country, city, email, username, password)
        """
            Check if the is old enough for our service
        """
        if(user.calculate_age() < 18 ):
            error = True
            flash('Sorry! You need to be at least 18 years old in order to register for this service :)')

        """
            Check if the user provided his country
        """
        if(len(user.country.strip()) < 2):
            error = True
            flash("Sorry! You need to provide your country's name with at least two characters")
        """
            Check if the user provided his city's name
        """
        if(len(user.city) < 2):
            error = True
            flash("Sorry! You need to provide your city's name with at least two characters")
        """
            Check if the user provided a correct email address
        """
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', user.email)
        if match == None:
            error = True
            flash("Sorry! You need to provide a correct email address")

        """
            Check if the user provided a password with at least 8 characters
        """
        if(len(user.password) < 8):
            error = True
            flash("Sorry! You need to provide a password with at least 8 characters")

        #I will check later if the password is strong enough

        check_user = User.query.filter_by(email = user.email).first()
        """
            Check if the email is available
        """
        if(check_user):
            error = True
            flash("Sorry! The email is not available!!!")

        """
            Check if the email is available
        """
        check_user = User.query.filter_by(username = user.username).first()
        if(check_user):
            error = True
            flash("Sorry! The username is not available!!!")

        """
            Check if we have latitude and longitude from the country and city
        """
        g = geocoder.google(user.city + ', ' + user.country)
        if(g.latlng == None):
            error = True
            flash("Sorry! The address you specified doesn't exist")

        user.latitude = g.latlng[0]
        user.longitude = g.latlng[1]
        nopic = 'no-pic.png'
        user.profile_picture = request.url_root + 'static/picture/' + nopic
        if(error != False):
            return redirect(url_for('index'))

        db.session.add(user)
        status = False

        try:
            if (UserNeo(graph=graph, username=username, latitude=g.latlng[0], longitude=g.latlng[1], gender = gender, age=user.calculate_age(), orientation = orientation, locationFormatted = city).register()):
                status = True

        except:
            flash("Error on user creation")
            formatted_lines = traceback.format_exc().splitlines()
            for line in formatted_lines:
                flash(line)
            db.session.close()
            return redirect(url_for('index'))

        if(status == True):
            session['username'] = username
            session['logged_in'] = True
            db.session.commit()

    except:
        flash('Error processing your request. Please try again.')
        db.session.close()
        return redirect(url_for('index'))

    db.session.close()
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email = request.form['emailusername']).first()
    password_signin = request.form['password-signin']
    status = False
    if user and bcrypt.check_password_hash(user.password, password_signin):
        session['username'] = user.username
        session['logged_in'] = True
        session['email'] = user.email
        if(user.profile_picture != None and len(user.profile_picture) > 0):
            session['profile_picture'] = user.profile_picture
        else:
            session['profile_picture'] = 'no-pic.png'
        status = True
    else:
        user = User.query.filter_by(username=request.form['emailusername']).first()
        if user and bcrypt.check_password_hash(user.password, password_signin):
            session['username'] = user.username
            session['logged_in'] = True
            session['email'] = user.email
            if(user.profile_picture != None and len(user.profile_picture) > 0):
                session['profile_picture'] = user.profile_picture
            else:
                session['profile_picture'] = 'no-pic.png'
            status = True
    if(status == False):
        flash('Login failed! Invalid username/password.')
        return redirect(url_for('index'))
    """
        Create the session variables to log in the user
    """
    # login_user(user, session)
    return redirect(url_for('dashboard'))

@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """ profile """
    if(not is_authenticated(session)):
        flash('Sorry! You need to log in order to access to this page!')
        return redirect(url_for('index'))
    username = session.get('username')
    user = User.query.filter_by(username = username).first()
    if request.method == 'POST':
        file = request.files['profile_picture']
        filename = ""
        if file and allowed_file(file.filename):
            filename = str(username) + '.' + secure_filename(file.filename).split(".")[-1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        orientation = request.form['orientation']
        gender = request.form['gender']
        # sexPreference = request.form['sexPreference']
        age_range_min = request.form['age_range_min']
        age_range_max = request.form['age_range_max']
        body_type = request.form['body_type']
        drinking = request.form['drinking']
        smoking = request.form['smoking']
        educationValue = request.form['educationValue']
        heightCm = request.form['heightCm']
        birth_date_submit = request.form['birth_date']
        country = request.form['country']
        city = request.form['city']
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        error = False
        #Validate the entered values
        if(len(country.strip()) < 2):
            error = True
            flash("Sorry! You need to provide your country's name with at least two characters")
        """
            Check if the user provided his city's name
        """
        if(len(city.strip()) < 2):
            error = True
            flash("Sorry! You need to provide your city's name with at least two characters")
        """
            Check if the user provided a correct email address
        """
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', user.email)
        if match == None:
            error = True
            flash("Sorry! You need to provide a correct email address")

        g = geocoder.google(city + ', ' + country)
        if(g.latlng == None):
            error = True
            flash("Sorry! The address you specified doesn't exist")

        if(len(password) > 0 and password != password_repeat):
            error = True
            flash("Sorry! You have to repeat the same password")

        if(error != False):
            return redirect(url_for('profile'))

        user.country = country
        user.city = city
        user.latitude = g.latlng[0]
        user.longitude = g.latlng[1]
        if( user.profile_picture == None):
            filename = 'no-pic.png'
        user.profile_picture = request.url_root + 'static/picture/' + filename
        user.orientation = orientation
        user.gender = gender
        birth_date = datetime.datetime.strptime(birth_date_submit, "%Y-%m-%d")
        user.birth_date = birth_date
        user.email = email
        if(len(password) > 0 ):
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_neo = UserNeo(graph=graph, username=username, latitude=g.latlng[0], longitude=g.latlng[1],
            minAge = age_range_min, maxAge = age_range_max, gender = gender, age=user.calculate_age(),
            orientation = orientation, locationFormatted = city,
            bodyType = body_type, drinking = drinking,
            educationValue = educationValue, smoking = smoking, height = heightCm)
        user_neo.register()
        db.session.commit()
        return redirect(url_for('dashboard'))
    user_neo = UserNeo(graph, username = user.username, latitude = 0, longitude = 0).find()
    age_range = []
    if(user_neo == None or user_neo['minAge'] == None):
        today = date.today()
        age = today.year - user.birth_date.year - ((today.month, today.day) < (user.birth_date.month, user.birth_date.day))
        age_range.append(28)
        age_range.append(age+10)
    else:
        age_range = user_neo['minAge'], user_neo['maxAge']

    return render_template('profile.html',
        current_user = user,
        age_range_min = age_range[0],
        age_range_max = age_range[1],
        usernode = user_neo
        )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/logout')
def logout():
    logout_user(session)
    return redirect(url_for('index'))

@app.route('/like/<username>')
def like(username):
    currentUsername = session.get('username')
    currentUserNeo = UserNeo(graph=graph, username=currentUsername)
    currenUser = User.query.filter_by(username = currentUsername).first()
    userLiked = User.query.filter_by(username = username).first()
    if (currentUserNeo.find()) is not None:
        if(userLiked is not None):
            userLikedNeo = UserNeo(graph=graph, username=username)
            if (userLikedNeo.find()) is not None:
                currentUserNeo.like_user(username)
            else:
                return jsonify({'success':0, 'error': 'userLikedNeo not found'})
        else:
            return jsonify({'success':0, 'error': 'userLiked not found'})
    else:
        return jsonify({'success':0, 'error': 'userNeo not found'})

    msgStr = "User " + currentUsername + " liked " + username
    matched = 0
    if (currentUserNeo.check_if_match(username)):
        match = Match(True, currenUser.id, userLiked.id)
        db.session.add(match)
        db.session.commit()
        db.session.close()
        matched = 1

    return jsonify({'success': 1, 'matched':matched, 'message': msgStr})

@app.route('/my_matches', methods=['GET', 'POST'])
def my_matches():
    """ my_matches """
    if(not is_authenticated(session)):
        flash('Sorry! You need to log in order to access to this page!')
        return redirect(url_for('index'))
    currentUsername = session['username']
    currentUserNeo = UserNeo(graph=graph, username=currentUsername)

    matches = []
    matchesLocations = []
    matchesAges = []
    matchesDistances = []
    matchesUsernames = []
    matchesPictures = {}
    matchesArray = []
    userN = currentUserNeo.find()
    if userN is not None:
        matches = currentUserNeo.get_matches()
        for node in matches:
            if node["username"] is not None:
                matchesArray.append(node)
            matchesUsernames.append(node["username"])
            matchesLocations.append(node["locationFormatted"])
            matchesAges.append(node["age"])
            matchesDistances.append(node["Distance"])
        matchesPictures = get_profile_pictures(matchesUsernames)

    user = User.query.filter_by(username = session['username']).first()

    return render_template('matches.html', current_user = user, matchesPictures = matchesPictures, matchesUsernames=matchesUsernames, matchesLocations=matchesLocations,matchesAges=matchesAges,matchesDistances=matchesDistances)

@app.route('/filter/', methods=["POST"])
def filter():
    if request.method == "POST":
        currentUsername = session.get('username')
        currentUserNeo = UserNeo(graph=graph, username=currentUsername)
        if (currentUserNeo.find()) is not None:
            jsonData = request.get_json()
            startFrom = 0
            if 'startFrom' in jsonData:
                startFrom = jsonData['startFrom']
            lookingFor = jsonData['lookingFor']
            interestedIn = jsonData['interestedIn']
            ageMax = jsonData['ageMax']
            ageMin = jsonData['ageMin']
            rangeDistance = jsonData['rangeDistance']

            matches = currentUserNeo.get_browse_nodes(distance = rangeDistance, gender=lookingFor, orientation = None, sexPreference = interestedIn, minAge = ageMin, maxAge = ageMax, startFrom=startFrom)
            matchesPictures = {}
            matchesUsernames = []
            matchesLocations = []
            matchesAges = []
            matchesDistances = []
            matchesLikes = []
            for node in matches:
                matchesUsernames.append(node["username"])
                matchesLocations.append(node["locationFormatted"])
                matchesAges.append(node["age"])
                matchesDistances.append(node["Distance"])
                matchesLikes.append(node["Likes"])
            matchesPictures = get_profile_pictures(matchesUsernames)
            return jsonify({'success': 1, 'matchesUsernames':matchesUsernames, 'matchesPictures':matchesPictures, 'matchesAges': matchesAges, 'matchesDistances': matchesDistances, 'matchesLikes': matchesLikes, 'matchesLocations': matchesLocations })
        else:
            return jsonify({'success': 0, 'error':'Your user was not found. Check your session.'})

@app.route('/sendmessage/', methods=['GET', 'POST'])
def sendmessage():
    """ my_matches """
    jsonData = request.get_json()
    return jsonify({'success': 1, 'message': jsonData['message'] })

@app.route('/fullmap')
def fullmap():
    users = User.query.all()
    users_dict = []
    for user in users:
        lat = float(user.latitude)
        lng = float(user.longitude)
        users_dict.append( { 'icon': icons.dots.yellow, 'title': user.username + ' ' + str(lat) + ' ; ' + str(lng) ,
        'lat': lat,
        'lng': lng })
    cpt = len(users_dict)
    fullmap = Map(
        identifier="fullmap",
        varname="fullmap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat=23.6393252,
        lng=119.967072,
        markers = users_dict,
        zoom="8"
    )
    return render_template('fullmap.html', fullmap=fullmap, users_dict = users_dict)

@app.route('/getnewmessagesfrom/<username>')
def get_new_messages_from(username):
    session_username = session.get('username')
    receiver_user = User.query.filter_by(username = username).first()
    session_user = User.query.filter_by(username = session_username).first()
    match = Match.query.from_statement(text("SELECT * FROM match where (user_a_id=:ida AND user_b_id=:idb) OR (user_a_id=:idb AND user_b_id=:ida) ")).params(ida = session_user.id, idb = receiver_user.id).first()
    messages = Message.query.filter_by(match_id = match.id, receiver_id = session_user.id, delivered = False).all()
    if(len(messages) == 0):
        return jsonify({'success': 0, 'user': username})
    return jsonify({'success': 1, 'user': username, 'messages': messages})

@app.route('/get20q')
def get20q():
    questions = Question.query.all()
    randomQuestion = random.choice(questions)
    return jsonify({'success': 1, 'question': randomQuestion.text })

def get_profile_pictures(users):
    users_dict = {}
    for user in User.query.filter(User.username.in_(users)):
        users_dict[user.username] = user.profile_picture
    return users_dict

if __name__ == '__main__':
    app.run()
