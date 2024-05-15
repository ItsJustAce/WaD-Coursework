"""
Tomos Lock
tomoslock@hotmail.co.uk
Version 1
WorldHotels flask website for booking and managing hotels and their rooms
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import re
from sqlalchemy.orm import sessionmaker

from models import User

app = Flask(__name__)  

app.secret_key = 'secret'

#sqlalchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:adminpass@localhost/WaD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended for performance

db = SQLAlchemy(app)

# #mysqldb setup
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'adminpass'
# app.config['MYSQL_DB'] = 'WaD'
#
# db = MySQL(app)

if __name__ == "__main__":
    app.run(debug=True)

#run a query on the database
def query_db(model:object , filters=None) -> object:
    #begin a session for the query and bind it to the database
    Session = sessionmaker(bind=db.engine)
    session = Session()

    query = session.query(model)
    #check if there is filters and therefore filter the query
    if filters:
        query = query.filter_by(**filters)

    #return the FIRST element found
    result = query.first()  # Modify this to fetchall() if needed

    #end the session and return the findings
    session.close()
    return result

def writeDB(query: object) -> None:
    db.session.add(query)
    db.session.commit()


###page routing
#home page
@app.route("/")
@app.route("/index/")
@app.route("/home/")
def home():
    return render_template("index.html")

#login page
@app.route("/login/", methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        print("post!")
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("request!")
        username = request.form['username']
        password = request.form['password']

        account = query_db(User, filters={'email': username,'hashed_password': password})
        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['email'] = account.email
            session['username'] = account.username
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

        email_exists = query_db(User, filters={'email': email})
        username_exists = query_db(User, filters={'username': username})
        if email_exists:
            msg = 'Account already exists !'
        elif username_exists:
            msg = 'Username taken !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[0-9]', tel):
            msg = 'Phone number must have only 11 numbers !'
        elif not username or not password or not email or not tel:
            msg = 'Please fill out the form !'
        else:
            #create user object to commit to database
            user = User(
                email=email,
                phone_number=tel,  # Assuming 'tel' contains a phone number (integer)
                hashed_password=password,
                username=username
            )
            writeDB(user)

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