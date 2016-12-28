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
        birth_date = datetime.datetime.strptime(request.form['birth_date_submit'], "%Y-%m-%d")
        country = request.form['country']
        city = request.form['city']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user = User(preference, gender, birth_date, country, city, email, password)
        if(user.calculate_age() < 18 ):
            flash('Sorry! You need to be at least 18 years old in order to register for this service :)')
            return redirect(url_for('index'))
        db.session.add(user)
        db.session.commit()
        flash('You have been registered with success')
        db.session.close()
    return render_template('dashboard.html')

@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})


@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})


@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})


if __name__ == '__main__':
    app.run()
