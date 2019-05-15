from rwolff.forms import RegistrationForm, projectForm, LoginForm
from rwolff.models import userPageView, User
from rwolff import app, db, bcrypt
from flask import Flask, render_template, url_for, flash, redirect, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required
import datetime as dt
import functools
import secrets

def tracker(func):
    @functools.wraps(func)
    def wrapper():
        #Only track user id if they are authenticated
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            user_id = None

        #Get session id if it exists; Reminder, session id lasts 8 years or until cookies are deleted
        session_id = session.get('FVID')

        # Get To URL
        base_url = request.base_url

        # Get From Url
        referrer_url = request.referrer if request.referrer else 'None'

        # get user agent
        user_agent = request.headers.get('User-Agent')

        # If no session data, then create new session data
        if session.get('FVID') is None:
            session['FVID'] = secrets.token_hex(32)
            session_id = session.get('FVID')

        # If user is clicking an outbound link, track this instead out /outboundLinks
        to_url = request.args.get('url', default=None, type=None) if base_url == request.url_root + 'outboundLinks' else base_url

        pv = userPageView(session_id = session_id, from_page = referrer_url, to_page = to_url, user_id = user_id, user_agent = user_agent)
        db.session.add(pv)
        db.session.commit()
        x = func()
        return x
    return wrapper


@app.route('/')
@tracker
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
@tracker
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/projects")
@tracker
@login_required
def projects():
    projects=None
    return render_template('projects.html',projects=projects)

@app.route("/addProject", methods=['GET', 'POST'])
def addProject():
    form = projectForm()
    if form.validate_on_submit():
        flash(f'Project created for {form.title.data}!', 'success')
        return redirect(url_for('projects'))
    return render_template('addProject.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
@tracker
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
@tracker
def about():
    age = dt.datetime.utcnow().year -dt.datetime(1985,10,4).year
    return render_template('about.html',title='About Me',age=age)

@app.route('/resume')
@tracker
def resume():
    return render_template('resume.html',title='Resume')

@app.route('/outboundLinks')
@tracker
def outboundLinks():
    url = request.args.get('url', default=None, type=None)
    return redirect(url)

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
