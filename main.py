from flask import Flask, redirect, url_for, session, render_template, request, flash
from flask_session import Session
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import os

# import other files from subfolders/modules
import model.model as model
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
        
        # verify user credentials against the database
        verified = model.verify_user(email, pw)
        
        if verified == True:
            # flash success message  
            flash("Login successful", "success")
                 
            # create session for user with burnout_score and feedback initialized
            session['user'] = {
                'email': email,
                'burnout_score': 0,
                'feedback': "",
                "category": ""
            }
        
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
        
        # FIX: removed duplicate password hashing here since add_user() already hashes it
        # save user to sqlite database (add_user will hash the password)
        user_id = db.add_user(email, raw_pw)
        
        # FIX: check if user creation was successful (not None due to duplicate email)
        if user_id is None:
            flash("Email already exists. Please sign in instead.", "error")
            return redirect(url_for("signin"))
        
        # create session for user with burnout_score and feedback initialized
        session['user'] = {
            'email': email,
            'burnout_score': 0,
            'feedback': "",
            "category": ""
        }
        
        return redirect(url_for("home"))
    
    return render_template("signup.html")

@app.route('/logout')
def logout():
    # clear the session to log out the user
    session.clear()
    
    return redirect(url_for("signin"))

@app.route("/home")
def home():
    # check if user is logged in
    if 'user' not in session:
        return redirect(url_for('signin'))
    
    # get score and feedback from session
    user = session['user']
    email = user['email']
    score = user.get('burnout_score', 0)  # default to 0 if not found
    feedback = user.get('feedback', "")    # default to empty string if not found
    category = user.get("category", "")
    
    return render_template("home.html", score=score, feedback=feedback, category=category)

@app.route("/track", methods=['GET', 'POST'])
def track():
    if request.method == "POST":
        # get form data from user input
        sleep = request.form["sleep"]
        mood = request.form["mood"]
        physical_activity = request.form["physical-activity"]
        water_intake = float(request.form["water"])
        caffeine_intake = float(request.form["caffeine"])
        last_meal_raw = request.form["last_meal"]
        # convert last meal to proper datetime format for sqlite storage
        last_meal = datetime.fromisoformat(last_meal_raw).strftime("%Y-%m-%d %H:%M:%S")
        
        # get user email from session
        email = session['user']['email']
        
        # verify user exists in database
        user = db.user_by_email(email)  # fetch user record from sqlite
        if not user:
            flash("User not found", "error")
            return redirect(url_for("signin"))
        
        # count how many meals the user has logged today using email
        num_meals = db.find_meals(email)
        
        # set data to dictionary for feedback generation
        data = {
            "sleep_range": sleep,
            "user_mood": mood,
            "physical_activity": physical_activity,
            "water_intake": water_intake,
            "caffeine_amount": caffeine_intake,
            "meals_taken": num_meals
        }
        
        # calculate burnout score and category based on user inputs
        burnout_rate = bs.compute_burnout_rate(sleep, mood, physical_activity, water_intake, caffeine_intake, num_meals)
        category = bs.burnout_category(burnout_rate)
        feedback = fb.generate_feedback(data, burnout_rate)
        
        # save daily input to sqlite database using user_email (not user_id)
        db.add_daily_input(email, sleep, mood, physical_activity, water_intake, caffeine_intake, last_meal, burnout_rate, datetime.now())
        
        # update session with new feedback and score
        session['user']['feedback'] = feedback
        session['user']['burnout_score'] = burnout_rate
        session['user']['category'] = category
        
        # redirect with score to display on home page
        return redirect(url_for("home"))
    
    return render_template("track.html")

@app.route("/profile")
def profile():
    # get user email from session
    user_email = session['user']['email']
    # mask password with bullets for display purposes
    user_pw_str = "•"*8  # FIX: changed from special character to normal bullet
    
    return render_template("profile.html", email=user_email, pw_string=user_pw_str)

if __name__ == "__main__":
    # initialize the sqlite database before running the app
    init_db.init_db()
    app.run(debug=True, port=5002)