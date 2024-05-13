"""
Tomos Lock
tomoslock@hotmail.co.uk
Version 1
WorldHotels flask website for booking and managing hotels and their rooms
"""

from flask import Flask, render_template
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

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