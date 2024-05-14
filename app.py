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

 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'adminpass'
app.config['MYSQL_DB'] = 'WaD'

db = MySQL(app)

if __name__ == "__main__":
    app.run(debug=True)

#run a query on the database
def queryDB(query: str) -> tuple:
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    return cursor.fetchall()

#page routing
@app.route("/")
@app.route("/index/")
@app.route("/home/")
def home():
    return render_template("index.html")

@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/account/")
def account():
    name = "balls"
    return render_template("account.html", name=name)

@app.route("/DBTEST/")
def dbtest():
    result = queryDB('SELECT * FROM users;')
    return result[0]