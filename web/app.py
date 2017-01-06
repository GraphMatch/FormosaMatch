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

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config['DEBUG'] = True
app.config['MAIL_DEBUG'] = True

graph = Graph('http://neo4j:admin123@neo4j:7474/db/data/')
# graph = Graph(host='192.168.99.100', http_port=7474, https_port= 7473, bolt_port=7687, user='neo4j', password='admin123')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)

from modelssql.user import User
from modelssql.token import generate_confirmation_token, confirm_token
from modelssql.email import send_email
from modelsneo.user import User as UserNeo


@app.route('/', methods=['GET', 'POST'])
def index():
    """ index handler """
    if(is_authenticated(session)):
        return redirect(url_for('dashboard'))
    """
        Try to get the country and city from the user IP address
    """
    ip = request.remote_addr #'140.114.202.215'
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
    user = User.query.filter_by(username = session['username']).first()
    return render_template('dashboard.html',current_user = user )


@app.route('/register', methods=['POST'])
def register():
    preference = request.form['preference']
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
        user = User(preference, gender, birth_date, country, city, email, username, password)
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

        if(error != False):
            return redirect(url_for('index'))

        db.session.add(user)
        status = False

        try:
            if (UserNeo(graph=graph, email=email, username=username, latitude=g.latlng[0], longitude=g.latlng[1]).register()):
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
        if(user.profile_picture is None) or (len(user.profile_picture) > 0):
            session['profile_picture'] = user.profile_picture
        else:
            session['profile_picture'] = 'default.jpg'
        status = True
    else:
        user = User.query.filter_by(username=request.form['emailusername']).first()
        if user and bcrypt.check_password_hash(user.password, password_signin):
            session['username'] = user.username
            session['logged_in'] = True
            session['email'] = user.email
            if(user.profile_picture is None) or (len(user.profile_picture) > 0):
                session['profile_picture'] = user.profile_picture
            else:
                session['profile_picture'] = 'default.jpg'
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
            filename = str(uuid.uuid1()) + '.' + secure_filename(file.filename).split(".")[-1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        preference = request.form['preference']
        gender = request.form['gender']
        sex_interest = request.form['sex_interest']
        age_range_min = request.form['age_range_min']
        age_range_max = request.form['age_range_max']
        search_distance = request.form['search_distance']
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
        user.profile_picture = filename
        user.preference = preference
        user.gender = gender
        birth_date = datetime.datetime.strptime(birth_date_submit, "%Y-%m-%d")
        user.birth_date = birth_date
        user.email = email
        if(len(password) > 0 ):
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        age_interest = str(age_range_min) + '-' + str(age_range_max)
        user_neo = UserNeo(graph, email, username, preference, sex_interest, search_distance, age_interest, country, city, g.latlng[0], g.latlng[1])
        user_neo.register()
        db.session.commit()
        return redirect(url_for('dashboard'))
    user_neo = UserNeo(graph, user.email).find()
    age_range = []
    if(user_neo == None):

        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_range.append(28)
        age_range.append(age+10)

    else:
        age_range = user_neo['age_interest'].split('-')

    return render_template('profile.html',
        user = user,
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

if __name__ == '__main__':
    app.run()
