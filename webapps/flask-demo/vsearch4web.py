from flask import Flask, render_template, request, session
from html import escape
from vsearch import vsearch
from auth_check import auth_check

app = Flask(__name__)
app.secret_key = 'TestingFlaskDemo'  # Replace with

def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

@app.route('/')
def home() -> str:
    return 'Welcome to search4letters on the web!'

@app.route('/')
@app.route('/entry')
def entry_page() -> str:
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')

@app.route('/search4', methods=['POST'])
def search4() -> str:
    the_results = str(vsearch(request.form['phrase'], request.form['letters']))
    log_request(request, the_results)
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
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=contents)

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
