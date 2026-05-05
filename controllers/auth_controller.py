from flask import url_for, redirect, session
from utils import oauth

def google_login():
    redirect_uri = url_for('auth.google_callback_route', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

def google_callback():
    token = oauth.google.authorize_access_token()
    user = oauth.google.userinfo()

    session['user'] = {
        'id': user.get('sub'),
        'email': user.get('email'),
        'name': user.get('name'),
        'picture': user.get('picture')
    }


    return redirect('/')

def logout():
    session.pop('user', None)
    return redirect('/')
