from flask import Flask, render_template, redirect, url_for, request

# create flask app
app = Flask(__name__)

# config for app
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'