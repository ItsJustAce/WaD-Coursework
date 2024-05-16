"""
Tomos Lock
tomoslock@hotmail.co.uk
Version 1
WorldHotels flask website for booking and managing hotels and their rooms
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import re
from sqlalchemy.orm import sessionmaker
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import join
import calculate
import datetime
from models import User, City, RoomType, Booking, Feature
import models
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  

admin = Admin(app)
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

class UserView(ModelView):

    def is_accessible(self):
        if session.get('username') == "admin":
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin.add_view(UserView(User, db.session))
admin.add_view(UserView(City, db.session))
admin.add_view(UserView(Booking, db.session))



# Create all tables
def create_tables():
    models.Base.metadata.create_all(bind=db.engine)

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
@app.route("/home/", methods =['GET', 'POST'])
def home():
    create_tables()
    if request.method == 'POST':
        if not session.get('loggedin'):
            print("not logged in!"  )
            return render_template('login.html', msg = "Please log in before attempting to search!")
        
        elif 'type' in request.form and 'city' in request.form and 'in' in request.form and 'out' in request.form:
            print("request!")
            type = request.form['type']
            city = request.form['city']
            checkin = request.form['in']
            checkout = request.form['out']

            user = db.session.query(User).filter_by(id=session.get('id')).first() 
            selected_city = db.session.query(City).filter_by(name=city).first()  
            pricing = selected_city.peak # change to select based on month
            today_date = datetime.date.today()
            booking_date = datetime.datetime.strptime(checkin, '%Y-%m-%d').date() # Replace with booking date
            checkout_date = datetime.datetime.strptime(checkout, '%Y-%m-%d').date() # Replace with booking date

            total = calculate.calculate_booking_price(pricing, booking_date, today_date)
            total = total * (checkout_date - booking_date).days # calculate how many days to charge per night

            booking = Booking(user_id=user.id, city_id=selected_city.id, check_in=checkin, check_out=checkout, total_price=total)
            
            # Add the booking to the session and commit changes
            db.session.add(booking)
            db.session.commit()
            print(type, city)
            return render_template("confirmation.html", booking=booking, city=selected_city.name, type=type)
    return render_template("index.html")
#reset password page
@app.route("/reset/", methods =['GET', 'POST'])
def reset():
    if request.method == 'POST' and 'password' in request.form:
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        account = query_db(User, filters={'id': session.get('id')})
        print(account)
        account.hashed_password = hashed_password
        print(account.hashed_password)

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('reset.html')
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

        account = query_db(User, filters={'email': username,'hashed_password': check_password_hash(password)})
        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['email'] = account.email
            session['username'] = account.username
            msg = 'Logged in successfully !'
            return redirect(url_for('account'))
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
                hashed_password=generate_password_hash(password),
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
        user_id = session['id']
        # bookings = db.session.query(Booking).filter_by(user_id=user_id).all()
        # bookings = db.session.query(Booking).filter_by(user_id=user_id)\
        # .join(City).filter_by(id=Booking.city_id).all()

        bookings = db.session.query(Booking) \
            .filter_by(user_id=user_id) \
            .all()
        return render_template('account.html', name=name, bookings=bookings)
    else:
        msg = "Please log in before viewing your account."
        return render_template('login.html', msg = msg)

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
  booking = query_db(Booking, filters={'id': booking_id})
  if booking and booking.user_id == session.get('id'):  # Check user ownership
    booking.is_cancelled = True
    db.session.delete(booking)
    db.session.commit()
    print("Cancelled")
    db.session.commit()

    return redirect(url_for('account'))  # Redirect back to account page
  else:
    flash('Error: Invalid booking or unauthorized cancellation.')
    return redirect(url_for('account'))

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