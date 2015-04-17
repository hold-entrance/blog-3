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
import time
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
# show posts
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM posts')
    posts = [dict(poster=row[0], post=row[1], datestr=row[2], timestr=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

@app.route('/add', methods=['POST'])
@login_required
def add():
    poster = request.form['poster']
    post = request.form['post']
    # Determine strings for date and time 
    totime = time.localtime(time.time())
    datestr = str(totime.tm_mon)+"-"+str(totime.tm_mday)+"-"+str(totime.tm_year)
    ampm = ""
    timestr = ""
    if totime.tm_hour == 0:
        ampm = "AM"
        timestr = str(totime.tm_hour+12)+":"+str(totime.tm_min)+" "+ampm
    elif totime.tm_hour != 0 and totime.tm_hour < 12:
        ampm = "AM"
        timestr = str(totime.tm_hour)+":"+str(totime.tm_min)+" "+ampm
    elif totime.tm_hour == 12:
        ampm = "PM"
        timestr = str(totime.tm_hour)+":"+str(totime.tm_min)+" "+ampm
    elif totime.tm_hour > 12:
        ampm = "PM"
        timestr = str(totime.tm_hour-12)+":"+str(totime.tm_min)+" "+ampm
    # Check to make sure other fields are populated with data
    if not poster or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO posts (name, post, date, time) VALUES (?, ?, ?, ?)', [poster, post, datestr, timestr])
        g.db.commit()
        g.db.close()
        flash('Your entry has been successfully posted. Thanks for your contribution, '+poster+'!')
        return redirect(url_for('main'))
        

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
