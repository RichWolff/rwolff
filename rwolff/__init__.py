from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from flask_bcrypt import Bcrypt

app = Flask(__name__)

u = 'richwolff'
p = '97a101e105i*'
h = 'richwolff-1160.postgres.pythonanywhere-services.com'
port = '11160'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{:}:{:}@{:}:{:}/wolff'.format(u,p,h,port)
app.config['SECRET_KEY'] = 'e71b4f38dd5eb138f941907ec7ea6c06'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=2922) # Set for 8 Years (8 * 365 + 2 leap year days)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

from rwolff import routes