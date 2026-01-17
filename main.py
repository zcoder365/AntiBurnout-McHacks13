from flask import Flask, redirect, url_for, session, render_template, request
from flask_session import Session
from authlib.integrations.flask_client import OAuth
import os

# create flask app
app = Flask(__name__)

# config for app
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # initialize flask-session

# ⚡ auth0 setup ======================================
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.environ['AUTH0_CLIENT_ID'],
    client_secret=os.environ['AUTH0_CLIENT_SECRET'],
    api_base_url=f"https://{os.environ['AUTH0_DOMAIN']}",
    access_token_url=f"https://{os.environ['AUTH0_DOMAIN']}/oauth/token",
    authorize_url=f"https://{os.environ['AUTH0_DOMAIN']}/authorize",
    client_kwargs={'scope': 'openid profile email'},
)

# ROUTES =============================================
@app.route("/")
def landing():
    return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return ""

@app.route("/callback")
def callback():
    token = auth0.authorize_access_token()
    user = auth0.parse_id_token(token)
    
    # store the user in session
    session['user'] = {
        'id': user['sub'],    # unique auth0 id
        'email': user['email'],
        'name': user.get('name', '')
    }
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    
    return redirect(
        f"https://{os.environ['AUTH0_DOMAIN']}/v2/logout?returnTo=http://localhost:5000"
    )

@app.route("/home")
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    return f"Welcome {user['name']} ({user['email']})! Your burnout dashboard goes here."