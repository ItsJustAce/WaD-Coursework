"""
Tomos Lock
tomoslock@hotmail.co.uk
Version 1
WorldHotels flask website for booking and managing hotels and their rooms
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_admin import Admin
import MySQLdb.cursors
import re

app = Flask(__name__)  

app.secret_key = 'secret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'adminpass'
app.config['MYSQL_DB'] = 'WaD'

db = MySQL(app)

if __name__ == "__main__":
    app.run(debug=True)

#run a query on the database
def queryDB(query):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    return cursor.fetchone()

def writeDB(query):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    db.connection.commit()
    return True

#page routing
@app.route("/")
@app.route("/index/")
@app.route("/home/")
def home():
    return render_template("index.html")

@app.route("/login/", methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        print("post!")
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("request!")
        username = request.form['username']
        password = request.form['password']
        query = f'SELECT * FROM users WHERE email = "{username}" AND hashed_password = "{password}"'
        account = queryDB(query)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('login.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


#register user
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        tel = request.form['tel']

        query = f'SELECT * FROM users WHERE username = "{username}"'
        account = queryDB(query)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[0-9]', tel):
            msg = 'Phone number must have only 11 numbers !'
        elif not username or not password or not email or not tel:
            msg = 'Please fill out the form !'
        else:
            query = f'INSERT INTO users VALUES (NULL, "{email}", "{tel}", "{password}", "{username}" )'
            writeDB(query)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

#redirect if not logged in
@app.route("/account/")
def account():
    if session.get('loggedin') == True:
        name = session['username']
        return render_template("account.html", name=name)
    else:
        msg = "Please log in before viewing your account."
        return render_template('login.html', msg = msg)

#remove user from session and redirect to login
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#DB testing purposes ONLY
# @app.route("/DBTEST/")
# def dbtest():
#     result = queryDB('SELECT * FROM users;')
#     return result[0]