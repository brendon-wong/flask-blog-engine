import os
import sqlite3

from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash)

# Create application instance
app = Flask(__name__)
# Load config from this file
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(
    DATABASE = os.path.join(app.root_path, 'blog.db'),
    SECRET_KEY= "Don't use insecure keys in production",
    USERNAME='admin',
    PASSWORD='default'
)
app.config.from_envvar('BLOG_SETTINGS', silent=True)


# Database connections

def connect_db():
    """Connect to app database"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# This decorator registers a new command with the flask script
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database"""
    init_db()
    print('Successfully initialized the database.')

def get_db():
    """Opens a new database connection if one is not present in the current
    application context"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# This decorates calls the close_db function whenever the app context tears down
@app.teardown_appcontext
def close_db(error):
    """Closes the database at the end of the request"""
    if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()


# View functions

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    # ? mark formatting is SQL injection protection with SQLite3
    db.execute('insert into entries (title, text) values (?, ?)',
             [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
