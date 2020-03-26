from flask import Flask
import flask_mongoengine as me
from flask_login import LoginManager
import os

db = me.MongoEngine()

def create_app():
    app = Flask(__name__, instance_relative_config = False, template_folder='../frontend')
    app.config['SECRET_KEY'] = "vnkdjnfskndl1232#"
    app.debug = True
    app.config['MONGODB_SETTINGS'] = {'host' : os.environ['MONGODB_URI']}
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import Agent

    @login_manager.user_loader
    def load_user(agent_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Agent.objects.get(id = agent_id)
    
    with app.app_context():
        from . import auth
        app.register_blueprint(auth.auth)
        return app
