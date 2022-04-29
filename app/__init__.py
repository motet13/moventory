from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_jsglue import JSGlue


movintoryApp = Flask(__name__)
movintoryApp.config.from_object(Config)
movintoryApp.config['MAX_CONTENT_LENGTH'] = 1000000
db = SQLAlchemy(movintoryApp)
ma = Marshmallow(movintoryApp)
jsglue = JSGlue(movintoryApp)
login = LoginManager(movintoryApp)
login.login_view = 'users.login'
login.login_message_category = 'info'

# Uncomment line below when starting a new db ########################################
# from app.models import User, Feedback, FeedbackSchema, Product, ProductSchema, Token
######################################################################################


from user_check import check_user
from app.main.routes import main
from app.users.routes import users
from app.managements.routes import managements
from app.recipes.routes import recipes
from app import error_handlers


check_user()
movintoryApp.register_blueprint(main)
movintoryApp.register_blueprint(users)
movintoryApp.register_blueprint(managements)
movintoryApp.register_blueprint(recipes)

