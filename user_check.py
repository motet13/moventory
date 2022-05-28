from app.models import User
from config import Config
from app import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

#Check database User table
#Only user admin should only exist in this table
#Implementation of limiting only one user (admin) to control application
def check_user():
    try:
        user = User.query.one()
    except MultipleResultsFound as e:
        print(f'{e} Exiting now...')
        quit()
    except NoResultFound:
        add_admin = User(username=Config.MOVENTORY_DEFAULT_USER, email=Config.MOVENTORY_DEFAULT_EMAIL)
        add_admin.set_password(Config.MOVENTORY_DEFAULT_PASSWORD)
        db.session.add(add_admin)
        db.session.commit()
    
    user = User.query.one()
    if user.id != 1 or user.username != 'admin':
        print('This user is not supposed to be in the database!')
        quit()