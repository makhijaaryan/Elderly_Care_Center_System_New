# this file makes the folder into a python package

from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import engine, text

load_dotenv()

db=SQLAlchemy()
DB_NAME="database.db"



def create_app():
    app=Flask(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    # from .models import Request, UserResident
    from .models import User, Note, Requests, Family,Log



    # create_database(app)

    with app.app_context():
        db.create_all()
        print("Database Created!")

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id_):
        # user=db.session.execute(text('select email from log where id=:id'),{'id':id_})
        user_type = db.session.execute(text('select role from log where id=:id'),{'id': id_})
        
        print(user_type.fetchone()[0])
        # if user_type=='resident':
            # res = db.session.execute(text('SELECT * FROM log natural join user where log.email=user.email '))
            # row = res.fetchone()  # Using fetchone() because we expect at most one result
            # return User.query.get(email=user.email)
        # res = db.session.execute(text('SELECT * FROM log natural join user where log.email=user.email '))
        # row = res.fetchone()  # Using fetchone() because we expect at most one result
        return Log.query.get(int(id_))
        # return row

    return app


# def create_database(app):
#     if not os.path.exists('website/'+DB_NAME):
#         # db.init_app(app)
#         # db.create_all(app)
#         db.create_all(app=app)
#         print("Database Created!")