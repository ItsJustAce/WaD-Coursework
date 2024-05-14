"""
Tomos Lock
tomoslock@hotmail.co.uk
Version 1
WorldHotels flask website for booking and managing hotels and their rooms
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
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


@app.route("/account/")
def account():
    name = session['username']
    return render_template("account.html", name=name)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/DBTEST/")
def dbtest():
    result = queryDB('SELECT * FROM users;')
    return result[0]