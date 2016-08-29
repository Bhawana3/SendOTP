from flask import Flask
import warnings
from flask.exthook import ExtDeprecationWarning

warnings.simplefilter('ignore', ExtDeprecationWarning)

#from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.secret_key = 'B0Zr98j/3yX R~XHH!jmN]LWX/,?RM'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/kisan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True					# to suppress warning at startup

engine = create_engine('mysql://root:password@localhost/kisan')
Session = sessionmaker (bind=engine)

db = SQLAlchemy(app)

CORS(app)

def register_blueprints(app):
    from .views import views
    app.register_blueprint(views)

register_blueprints(app)
