from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Agent
import mongoengine as me
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')
    
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    agent = Agent.objects.filter(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not agent or not check_password_hash(agent.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    login_user(agent, remember=remember)
    return redirect(url_for('route_blueprint_frontend.profile'))

@auth.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html')
    
    
@auth.route('/signup', methods=['POST'])
def signup_post():        
    agent = Agent()
    #refresh if fields are missing
    try:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
    except:
        return redirect(url_for('auth.signup_get'))
    
    #see if this agent already exists
    results = Agent.objects.filter(email=email).first()
    if results: # if an agent is found, refresh
        flash('Email address already exists')
        return redirect(url_for('auth.signup_get'))
    #try:
    agent.email = email
    agent.name = name
    agent.password = generate_password_hash(password, method='sha256')
    agent.save()
    #except:
    #    return "Error, please retry"    
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('route_blueprint_frontend.load_homepage'))

