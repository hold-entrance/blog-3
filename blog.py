# Flask Blog 3rd Attempt

# imports
from flask import Flask
from flask import render_template
from flask import request 
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
from flask import g
from functools import wraps
import os
import sqlite3

# configuration 
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = str(os.urandom(24))

app = Flask(__name__)

# pulls in configuration by looking for uppercase variables
app.config.from_object(__name__)

# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# setup 'sessions' via login_required decorator to protect main.html from unauthorized access
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# route and define the login page function
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'INVALID CREDENTIALS. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/main')
@login_required
def main():
    return render_template('main.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
