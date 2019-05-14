from rwolff.forms import RegistrationForm, projectForm, LoginForm
from rwolff.models import userPageView
from rwolff import app
from flask import Flask, render_template, url_for, flash, redirect, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import functools
import secrets

def tracker(func):
    @functools.wraps(func)
    def wrapper():
        session_id = session.get('FVID')
        base_url = request.base_url
        if session.get('FVID') is None:
            session['FVID'] = secrets.token_hex(32)
            session_id = session.get('FVID')

        to_url = request.args.get('url', default=None, type=None) if base_url == request.url_root + 'outboundLinks' else base_url
        print(userPageView(session_id=session_id,from_page = request.referrer,to_page=to_url,user_id=None))
        x= func()
        return x
    return wrapper


@app.route('/')
@tracker
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
@tracker
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/projects")
@tracker
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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

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
    print(url)
    return redirect(url)
