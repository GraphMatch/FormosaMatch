# app.py

"""#!/usr/bin/env python"""
""" application file """
from flask import Flask
from flask import request, redirect, session, abort, url_for, render_template, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from py2neo import Graph
from config import BaseConfig
import datetime
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(BaseConfig)


graph = Graph('http://neo4j:neo4j@192.168.99.100:7474/db/data/')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from modelssql.user import User

"""from modelsneo import *
from modelssql import *"""
@app.route('/', methods=['GET', 'POST'])
def index():
    """ index handler """
    #users = queries.get_users(graph)
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """ dashboard """
    #users = queries.get_users(graph)
    return render_template('dashboard.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        preference = request.form['preference']
        gender = request.form['gender']
        birth_date_submit = request.form['birth_date_submit']
        country = request.form['country']
        city = request.form['city']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        error = False
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

        if(error != False):
            return redirect(url_for('index'))
        db.session.add(user)
        db.session.commit()
        flash('You have been registered with success')
        session['username'] = username
        session['logged_in'] = True
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
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged off successfully')
    return redirect(url_for('index'))


@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})


if __name__ == '__main__':
    app.run()
