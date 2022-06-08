from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager


moventoryApp = Flask(__name__)
moventoryApp.config.from_object(Config)
moventoryApp.config['MAX_CONTENT_LENGTH'] = 1000000
db = SQLAlchemy(moventoryApp)
ma = Marshmallow(moventoryApp)
login = LoginManager(moventoryApp)
login.login_view = 'users.login'
login.login_message_category = 'info'

# Uncomment line below when starting a new db ########################################
# from app.models import User, Feedback, FeedbackSchema, Product, ProductSchema, Token
# db.create_all()
######################################################################################

from user_check import check_user
from app.main.routes import main
from app.users.routes import users
from app.managements.routes import managements
from app.recipes.routes import recipes
from app import error_handlers


check_user()
moventoryApp.register_blueprint(main)
moventoryApp.register_blueprint(users)
moventoryApp.register_blueprint(managements)
moventoryApp.register_blueprint(recipes)

