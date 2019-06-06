from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login.mixins import AnonymousUserMixin
from flask_share import Share
app = Flask(__name__)

u = 'richwolff'
p = '97a101e105i*'
h = 'richwolff-1160.postgres.pythonanywhere-services.com'
port = '11160'

track_pageviews = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{:}:{:}@{:}:{:}/wolff'.format(u,p,h,port)
app.config['SECRET_KEY'] = 'e71b4f38dd5eb138f941907ec7ea6c06'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=2922) # Set for 8 Years (8 * 365 + 2 leap year days)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db,compare_type=True)
Share(app)

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.is_contributor = False
    self.is_admin = False

login_manager = LoginManager(app)
login_manager.anonymous_user = Anonymous
login_manager.login_view = 'login'
login_manager.login_message = u"Please login to view that page."
login_manager.login_message_category = 'info'

from rwolff import routes