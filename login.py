from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__, template_folder='.')

# set the secret key. Keep this really secret:
app.secret_key = 'your_secret_key_here'

# define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # check if the user submitted the correct credentials
        if request.form['username'] == 'myuser' and request.form['password'] == 'mypassword':
            # if the credentials are correct, store the username in the session
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            # if the credentials are incorrect, show an error message
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# define the index route
@app.route('/')
def index():
    # check if the user is logged in
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# define the logout route
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))