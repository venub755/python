import logging
import os, sys
from html import escape

from flask import Flask, render_template, request, session

from auth_check import auth_check
from vsearch import vsearch
from AbstractFactoryDBContextManager import DBManagerFactory

app = Flask(__name__)
app.secret_key = 'TestingFlaskDemo'  # Replace with
app.logger.setLevel(logging.DEBUG)
app.logger.propagate = True
logging.basicConfig(level=logging.DEBUG, force=True)
db_type = os.environ.get("DB_TYPE", "mysql")
db_config = {}

def setup_db_config() -> dict:
    global db_config
    db_config = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "database": os.environ.get("DB_NAME", "vsearchlogdb"),
        "port": int(os.environ.get("DB_PORT", 3306)),
        "read_timeout": int(os.environ.get("DB_TIMEOUT", 10)),
        "write_timeout": int(os.environ.get("DB_TIMEOUT", 10)),
    }
    return db_config

def emit_debug(message: str) -> None:
    print(f"[FLASK DEBUG] {message}", file=sys.stderr, flush=True)

@app.route('/')
def home() -> str:
    return 'Welcome to search4letters on the web!'

@app.route('/')
@app.route('/entry')
def entry_page() -> str:
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')

@app.route('/search4', methods=['POST'])
def search4() -> str:
    _SQL = """insert into log
                (phrase, letters, ip, user_agent, results)
                VALUES (%s, %s, %s, %s, %s)"""
    the_results = str(vsearch(request.form['phrase'], request.form['letters']))
    db_config = setup_db_config()
    with DBManagerFactory.create_db_manager(db_type, db_config) as cursor:
        cursor.execute(_SQL, (request.form['phrase'], request.form['letters'], request.remote_addr, request.headers.get('User-Agent'), the_results))
    return render_template('results.html', 
                           the_title='Search Results', 
                           phrase=request.form['phrase'], 
                           letters=request.form['letters'], 
                           results=the_results
                           )

@app.route('/viewlog')
@auth_check
def view_the_log() -> 'html':
    contents = []
    emit_debug("Viewing log file")

    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html', the_title='View File Log', the_row_titles=titles, the_data=contents)

@app.route('/viewDBlog')
@auth_check
def view_the_DBlog() -> 'html':
    contents = []
    db_config = setup_db_config()
    emit_debug(f"DB Config: {db_config}")
    with DBManagerFactory.create_db_manager(db_type, db_config) as cursor:
        cursor.execute("SELECT phrase, letters, ip, user_agent, results FROM log")
        for row in cursor.fetchall():
            contents.append([escape(str(item)) for item in row])
    titles = ('Phrase', 'Letters', 'IP', 'User Agent', 'Results')
    return render_template('viewlog.html', the_title='View DB Log', the_row_titles=titles, the_data=contents)

@app.route('/login')
def login() -> 'html':
    session['user_id'] = 1  # Simulate a user login
    return render_template('login.html', 
                           the_title='Logged In', 
                           the_results='You are now logged in.'
                           )

@app.route('/logout')
def logout() -> 'html':
    session.pop('user_id') # Simulate a user logout
    return render_template('logout.html', 
                           the_title='Logged Out',
                           the_results='You are NOT logged in'
                           )

if __name__ == '__main__':
    app.run(debug=True)
