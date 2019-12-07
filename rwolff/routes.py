from rwolff.forms import RegistrationForm, projectForm, LoginForm, UpdateAccountForm, projectDetailsForm, postForm
from rwolff.models import userPageView, User, Projectheader, Projectdetails, Post, post_tags, Tags
from rwolff import app, db, bcrypt, track_pageviews
from flask import Flask, render_template, url_for, flash, redirect, request, make_response, session, jsonify, send_file, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from flask_login import login_user, current_user, logout_user, login_required
from slugify import slugify
from bs4 import BeautifulSoup
import datetime as dt
import functools
import secrets
import os
import glob
import re
from PIL import Image

def tracker(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
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

        resp = make_response(func(**kwargs))
        # If no session data, then create new session data
        if not 'FVID' in request.cookies:
            session_id = secrets.token_hex(32)
            resp.set_cookie(key='FVID',value=session_id, expires=dt.datetime.now()+dt.timedelta(2922))
        else:
            session_id = request.cookies['FVID']

        # If user is clicking an outbound link, track this instead out /outboundLinks
        to_url = request.args.get('url', default=None, type=None) if base_url == request.url_root + 'outboundLinks' else base_url
        pv = userPageView(session_id = session_id, from_page = referrer_url, to_page = to_url, user_id = user_id, user_agent = user_agent)
        if track_pageviews:
            db.session.add(pv)
            db.session.commit()
        else:
            print(pv)
        x = func(**kwargs)
        return resp
    return wrapper

def is_contributor(func):
    @functools.wraps(func)
    def wrapper():
        result = current_user.is_contributor
        if result:
            x = func()
            return x
        else:
            flash(f'You do not have permission to do that.', 'info')
            return redirect(url_for('home'))
    return wrapper


@app.route("/projects/add", methods=['GET', 'POST'])
@is_contributor
@login_required
def add_project():
    if request.method == 'POST':

        try:
            project = Projectheader(title = request.form['title'], description = request.form['description'], start_date = request.form['start_date'], end_date = request.form['end_date'],active_state=request.form['active_state'], Creator=current_user)
            db.session.add(project)
            db.session.flush()

            for k,v in request.form.items():
                if 'projectDesc' in k:

                    if v is None or v == '':
                        continue

                    projectDeet = Projectdetails(
                        project_id=project.id,
                        attr = "Detail",
                        value = v,
                        displayOrder = int(re.findall('[0-9]', k)[0])
                    )

                    db.session.add(projectDeet)

            db.session.commit()
            flash(f"Project created for {request.form['title']}!", 'success')

            return redirect(url_for('projects'))

        except Exception as e:
            print(e)
            db.session.rollback()
            flash(f'Failed to create project','failure')
    form = projectForm()
    formDetails = projectDetailsForm()
    formTags = projectDetailsForm()
    return render_template('addProject.html', title='New Project', form=form, legend='Create a New Project', project=None, formDetails=formDetails, formTags=formTags)

@app.route('/')
@tracker
def home():
    posts = Post.query.filter(Post.post_type=='Blog Post').order_by(Post.date_posted.desc()).limit(3).all()
    projects = Post.query.filter(Post.post_type=='Project').order_by(Post.date_posted.desc()).limit(3).all()
    return render_template('index.html', posts=posts, projects=projects)

@app.route("/register", methods=['GET', 'POST'])
@tracker
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,password=hashed_pwd,role=2)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/projects")
@tracker
def projects(**kwargs):
    tags = db.engine.execute("""
        Select
            tags.name,
            count(*) count
        FROM tags
        JOIN entry_tags
            ON tags.id = entry_tags.tag_id
        JOIN post
            ON entry_tags.post_id = post.id
        WHERE post.active_state = 'Active' and post.post_type = 'Project'
        GROUP BY tags.name""")
    if (kwargs.get('tag')):
        posts=Post.query.join(post_tags).join(Tags).filter(Tags.name==kwargs.get('tag')).all()
    else:
        posts=Post.query.filter(Post.post_type=='Project').order_by(Post.date_posted.desc()).all()
    return render_template('posts.html',posts=posts, tags=tags, content_type='Projects')

@app.route("/projects/<int:project_id>", methods=['GET', 'POST'])
def project(project_id):
    project = Projectheader.query.get_or_404(project_id)
    return render_template('project.html', title='Project',project=project)

@app.route("/projects/<int:project_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    project = Projectheader.query.get_or_404(project_id)
    if project.Creator != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Project Removed.', 'success')
    return redirect(url_for('projects'))


@app.route("/projects/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Projectheader.query.get_or_404(project_id)

    if project.Creator != current_user:
        abort(403)

    form = projectForm()
    formDetails = projectDetailsForm()
    formTags = projectDetailsForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.active_state = form.active_state.data
        db.session.commit()
        flash('Project has been updated', 'success')
        return redirect(url_for('project', project_id=project.id))

    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.start_date.data = project.start_date
        form.end_date.data = project.end_date
        form.active_state.data = project.active_state

    return render_template('addProject.html', title='Update Project', form=form, legend='Update Project',project = project, formDetails=formDetails, formTags=formTags)

def get_post_summary(content):
    soup = BeautifulSoup(content, 'html.parser')
    summary = soup.find('summary')
    if summary is None:
        return  content
    else:
        return summary.prettify()

##### Blog Post Routes #####
@app.route('/addPost', methods=['GET','POST'])
def add_post():
    form = postForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(
                title = form.title.data,
                content = form.content.data,
                active_state = form.active_state.data,
                post_type = form.post_type.data,
                Author = current_user,
                slug = slugify(request.form['title']) if form.slug.data == '' else form.slug.data,
                summary = get_post_summary(form.content.data),
                tags = form.tags.data
            )

            print(post)

            db.session.add(post)
            db.session.commit()
            flash(f"Post created for {request.form['title']}!", 'success')
            return redirect(url_for('update_post',post_id=post.id))
        else:
            flash(f'Failed to create post','failure')
    return render_template('addPost.html', title='New Post', form=form, legend='Create a New Post', post=None, images=postPhotoGallery())#formDetails=formDetails, formTags=formTags)

    #formDetails = projectDetailsForm()
    #formTags = projectDetailsForm()


@app.route("/posts")
@app.route("/posts/tag/<path:tag>")
@tracker
def posts(**kwargs):
    tags = db.engine.execute("""
        Select
            tags.name,
            count(*) count
        FROM tags
        JOIN entry_tags
            ON tags.id = entry_tags.tag_id
        JOIN post
            ON entry_tags.post_id = post.id
        WHERE post.active_state = 'Active' and post.post_type = 'Blog Post'
        GROUP BY tags.name""")
    if (kwargs.get('tag')):
        posts=Post.query.join(post_tags).join(Tags).filter(Tags.name==kwargs.get('tag')).all()
    else:
        posts=Post.query.filter(Post.post_type=='Blog Post').order_by(Post.date_posted.desc()).all()
    return render_template('posts.html',posts=posts, tags=tags, content_type='Blog Posts')

@app.route("/posts/<int:post_id>")
@app.route("/posts/<path:slug>")
@tracker
def post(**kwargs):
    blogPost = Post.query.filter( ((Post.id == kwargs.get('post_id')) | (Post.slug == kwargs.get('slug')))).first()
    return render_template('post.html', title='Post',blogPost=blogPost)

@app.route("/posts/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(**kwargs):
    blogPost = Post.query.filter((Post.id == kwargs.get('post_id')) | (Post.slug == kwargs.get('slug'))).first()

    images = postPhotoGallery()

    if blogPost.Author != current_user:
        abort(403)

    form = postForm()

    if form.validate_on_submit():
        print(get_post_summary(form.content.data))
        blogPost.title = form.title.data
        blogPost.content = form.content.data
        blogPost.active_state = form.active_state.data
        blogPost.post_type = form.post_type.data
        blogPost.slug = form.slug.data
        blogPost.tags = form.tags.data
        blogPost.summary = get_post_summary(form.content.data)
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('post', slug=blogPost.slug))

    elif request.method == 'GET':
        form.title.data = blogPost.title
        form.content.data = blogPost.content
        form.active_state.data = blogPost.active_state
        form.post_type.data = blogPost.post_type
        form.tags.data = blogPost.tags
        form.slug.data = blogPost.slug

    return render_template('addPost.html', title='Update Post', form=form, legend='Update Post', post=blogPost,images=postPhotoGallery())


@app.route("/posts/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.Author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Removed.', 'success')
    return redirect(url_for('posts'))



##### Account Register, Login, Logout, Etc ####
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


def save_account_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_post_pictures(form_picture):
    random_hex = secrets.token_hex(8)
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/imgs/posts', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn


def postPhotoGallery():
    homeDir = os.path.dirname(os.path.abspath(__file__))
    imgs = url_for('static',filename='imgs/posts')
    folder = os.path.join(homeDir+imgs)

    types = ('*.png', '*.jpg','*.gif','*.jpeg','*.PNG') # the tuple of file types
    files_grabbed = []

    for files in types:
        pathToFiles = os.path.join(folder,files)
        files_grabbed.extend(glob.glob(pathToFiles))

    files_grabbed = [os.path.basename(file) for file in files_grabbed]

    return files_grabbed

@app.route("/postUploadImages", methods=["GET","POST"])
def postUploadImages():
    files = request.files.getlist("file[]")
    if not files == []:
        uploaded_files = request.files.getlist("file[]")
        for file in uploaded_files:
            save_post_pictures(file)
        return render_template('upload.html')
    return render_template('upload.html')

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_account_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.nickname = form.nickname.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.nickname.data = current_user.nickname
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,form=form)

@app.route("/getSuperstoreData")
def getSuperstoreData():
    homeDir = os.path.dirname(os.path.abspath(__file__))
    superStoreFile = url_for('static',filename='superstore/P1-SuperStoreUS-2015.csv')

    folder = os.path.join(homeDir+superStoreFile)
    with open(folder,'r') as file:
        csv = file.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=superstore_data.csv"}
    )