from flask import Flask, redirect, url_for, session, render_template, request, flash
from flask_session import Session
from datetime import datetime
from dotenv import load_dotenv
import os
import model.model as model

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
    return redirect(url_for("login"))

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        pw = request.form.get("password")
        
        # verify user
        verified = model.verify_user(email, pw)
        
        if verified == True:
            # flash success message  
            flash("Login successful", "success")
                 
            # create session for user
            session['user'] = {'email': email}
        
            # redirect user to home page
            return redirect(url_for("home"))
        else:
            # flash error message
            flash("Email or password incorrect", "error")
            
            # redirect user to sign up page
            return redirect(url_for("signup"))
    
    return render_template("signin.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        raw_pw = request.form.get("password")
        
        # save user to database
        
        # create session for user
        session['user'] = {'email': email}
        
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
    
    # get score from database
    
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
        
        # call count_meal()
        num_meals = model.count_meals(session['user']['email'])
        
        # pass to score/feedback file
        
        # save to database
        
        # redirect with score to pass into html 
        return redirect(url_for("home"))
    
    return render_template("track.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)