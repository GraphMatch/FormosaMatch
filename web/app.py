# app.py

"""#!/usr/bin/env python"""
""" application file """
from flask import Flask
from flask import request, redirect, session, abort, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from py2neo import Graph

app = Flask(__name__)
app.config['DEBUG'] = True

graph = Graph('http://neo4j:neo4j@192.168.99.100:7474/db/data/')
db = SQLAlchemy(app)

from modelsneo import *
from modelssql import *
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


@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(
        email=json_data['email'],
        password=json_data['password']
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


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
