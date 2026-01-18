from flask import Flask, redirect, url_for, session, render_template, request, flash
from flask_session import Session
from datetime import datetime
from dotenv import load_dotenv
import bcrypt
import os
import model.model as model

# import other files from subfolders/modules
import model.database.init_db as init_db
import model.database.database as db
import model.feedback.burnout_score as bs
import model.feedback.feedback as fb

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
        # hash the user's password
        hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # save user to database
        db.add_user(email, hashed_pw)
        
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
    user = session['user']
    email = user['email']
    score = user['burnout_score']
    feedback = user['feedback']
    
    if feedback == None:
        feedback = ""
    
    return render_template("home.html", score=score, feedback=feedback)

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
        
        # get user ID
        user_id = db.user_by_email(session['user']['email'])
        
        # pass to score/feedback file to get score
        burnout_rate = bs.compute_burnout_rate(sleep, mood, physical_activity, water_intake, caffeine_intake, num_meals)
        feedback = bs.burnout_category(burnout_rate)
        
        # save to database/session
        db.add_daily_input(user_id, sleep, mood, physical_activity, water_intake, caffeine_intake, last_meal, datetime.now())
        session['user']['feedback'] = feedback
        session['user']['burnout_score'] = burnout_rate
        
        # redirect with score to pass into html 
        return redirect(url_for("home"))
    
    return render_template("track.html")

if __name__ == "__main__":
    # init_db.init_db()
    app.run(debug=True, port=5002)