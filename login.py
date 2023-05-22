from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)

app.secret_key = 'very secret'
# Enter your database connection details below

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'JALALASSS'
app.config['MYSQL_DB'] = 'pythonlogin'
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/MyWebApp/ - this will be the login page, we need to use both GET and POST #requests


@app.route('/MyWebApp/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,)) # SQL STORING
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # IMPLEMENT SECURITY FEATURE HERE, NOT SECURE
            # PYTHON HAS A DEFAULT SESSION COOKIE WITH FLASK, NO NID SQL QUERY LIKE THE REQUEST ONE ON TOP
            # UNDER INSPECT > APPLICATION > SESSION > STORED ON CLIENT
            # STORING SESSION COOKIE ON LOCAL AND SESSION STORAGE AND TURNING OFF THE DIFF FLAGS CAN BE A SECURITY FEATURE
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesn’t exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg='')


# http://localhost:5000/MyWebApp/logout - this will be the logout page
@app.route('/MyWebApp/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()


# do not put security features on client side because anyone can go in and turn it off.
# do on server and client
# ask elgin for diagram and which one is client and server
