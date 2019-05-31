from datetime import datetime
from rwolff import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120),nullable=True)
    last_name = db.Column(db.String(120),nullable=True)
    nickname = db.Column(db.String(120),nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    posts = db.relationship('Post', backref='Author', lazy=True)
    role = db.Column(db.Integer, nullable=True)
    projects = db.relationship('Projectheader', backref='Creator', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    roles = {
        0:'Admin',
        1:'Contributor',
        2:'Member'
    }

    def is_contributor(self):
        return self.role in (0,1)

    def is_admin(self):
        return self.role == 0

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    active_state = db.Column(db.String, nullable=True)
    details = db.relationship('PostDetails', backref='post', lazy=True)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class PostDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    attr = db.Column(db.String(25), nullable=False)
    value = db.Column(db.Text, nullable=False)
    displayOrder = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"PostDetails(post='{Post.Title}',attr='{self.attr}', value='{self.value}')"

class userPageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, nullable=False)
    from_page = db.Column(db.String, nullable=False)
    to_page =  db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user_agent = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"userPageView(session_id:'{self.session_id}', user_id:{self.user_id}, from_page:'{self.from_page}', to_page:'{self.to_page}', date/time:'{self.timestamp}')"

class Projectheader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_date = db.Column(db.DateTime,nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    active_state = db.Column(db.String, nullable=True)
    details = db.relationship('Projectdetails', backref='project', lazy=True, cascade="all,delete")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Projectheader(title='{self.title}', description='{self.description}', active_state={self.active_state})"

class Projectdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projectheader.id'), nullable=False)
    attr = db.Column(db.String(25), nullable=False)
    value = db.Column(db.Text, nullable=False)
    displayOrder = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Projectdetails(project_id='{self.project_id}', attr={self.attr}, value='{self.value}', displayOrder:{self.displayOrder}, last updated:'{self.date_last_update}')"
