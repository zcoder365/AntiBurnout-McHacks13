from flask import Flask, redirect, url_for, session, render_template, request
from flask_session import Session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # encrypt password
        
        # store in database
        
        return redirect(url_for("home"))
    
    return render_template("login.html")

# @app.route("/signup", methods=['GET', 'POST'])
# def signup():
#     return ""

@app.route("/callback")
def callback():
    token = auth0.authorize_access_token()
    user = auth0.parse_id_token(token)
    
    # extract user info
    auth0_id = user['sub']
    email = user['email']
    name = user.get('name', '')
    password = user['password']
    
    print("Collected data:", user, email)
    
    # 🆕 save to database (add this)
    db_user_id = get_or_create_user(auth0_id, email)
    
    # store in session (update this)
    session['user'] = {
        'auth0_id': auth0_id,
        'db_id': db_user_id,  # 🆕 add database id
        'email': email,
        'name': name
    }
    
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    
    return redirect(
        f"https://{os.environ['AUTH0_DOMAIN']}/v2/logout?returnTo={BASE_URL}"
    )

@app.route("/home")
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    return render_template("home.html")

@app.route("/track", methods=['GET', 'POST'])
def track():
    return render_template("track.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)