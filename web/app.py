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



graph = Graph('http://neo4j:neo4j@192.168.99.100:7474/db/data/')

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
    birth_date_submit = request.form['birth_date_submit']
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




        # token = generate_confirmation_token(user.email)
        # confirm_url = url_for('confirm_email', token=token, _external=True)
        # html = render_template('activate_user.html', confirm_url=confirm_url)
        # subject = "Please confirm your email"
        # send_email(user.email, subject, html)
        # flash('A confirmation email has been sent via email.', 'success')
        # flash('Success.', 'success')
        status = False
        try:
            db.session.add(user)
            # if (UserNeo(graph=graph, email=email, username=username, latitude=g.latlng[0], longitude=g.latlng[1]).register()):
            status = True
        except:
            traceback.print_exc(file=sys.stdout)
            # print (formatted_lines)
            # formatted_lines = traceback.format_exc().splitlines()
            # flash(formatted_lines)
            # flash('Error creating user on neo4j')

        if(status == True):
            flash('You have been registered with success')
            # flash('User node has been created with success')
            session['username'] = username
            session['logged_in'] = True
            db.session.commit()
        # else:
            # flash('Failed to create user node')



    except:
        flash('Error 666 processing your request. Please try again.')

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
        status = True
    else:
        user = User.query.filter_by(username=request.form['emailusername']).first()
        if user and bcrypt.check_password_hash(user.password, password_signin):
            session['username'] = user.username
            session['logged_in'] = True
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

@app.route('/logout')
def logout():
    logout_user(session)
    flash('You have been logged out successfully')
    return redirect(url_for('index'))
#
#
# @app.route('/api/status')
# def status():
#     return jsonify({'status': is_authenticated()})

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email = email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run()
