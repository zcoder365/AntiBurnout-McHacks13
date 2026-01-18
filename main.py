from flask import Flask, redirect, url_for, session, render_template, request
from flask_session import Session
from datetime import datetime
from dotenv import load_dotenv
import os
import model as model

BASE_URL = "http://localhost:5002"

# load data from .env file
load_dotenv()

# create flask app
app = Flask(__name__)

# config for app
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # initialize flask-session

# ROUTES =============================================
@app.route("/")
def landing():
    return redirect(url_for("signin"))

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        pw = request.form.get("password")
        
        # verify user + log them in (set the session to them)
        
        return redirect(url_for("home"))
    
    return render_template("signin.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        raw_pw = request.form.get("password")
        
        pw = "" # encrypt password
        
        # save user to database
        
        return redirect(url_for("home"))
    
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.clear()
    
    return redirect(url_for("signin"))

@app.route("/home")
def home():
    if 'user' not in session:
        return redirect(url_for('signin'))

    user = session['user']
    return render_template("home.html")

@app.route("/track", methods=['GET', 'POST'])
def track():
    if request.method == "POST":
        sleep = request.form.get("sleep")
        mood = request.form.get("mood")
        physical_activity = request.form.get("physical-activity")
        water_intake = request.form.get("water")
        caffeine_intake = request.form.get("caffeine")
        last_meal_raw = request.form.get("last_meal")
        last_meal = datetime.fromisoformat(last_meal_raw).strftime("%Y-%m-%d %H:%M:%S")
        
        # save to database
        
        # call count_meal()
        num_meals = model.count_meals(session['user']['email'])
        
        # pass to score/feedback file
        
        return redirect(url_for("home"))
    
    return render_template("track.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)