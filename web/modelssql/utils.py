
def login_user(user, session):
    session['logged_in'] = True
    #session['username'] = user.username

def logout_user(session):
    session.pop('logged_in', None)
    #session.pop('username', None)

def is_authenticated(session):
    if session.get('logged_in'):
        if session['logged_in']:
            return True
        return False
    else:
        return False
