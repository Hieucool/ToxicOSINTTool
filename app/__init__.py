from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path

import requests

def my_task():
    r =  requests.get("http://127.0.0.1:5000/cronjob")
    print('hi im running every 15 minutes')
    
from apscheduler.schedulers.background import BackgroundScheduler  
sched = BackgroundScheduler(daemon=True)
sched.add_job(my_task,'interval',minutes=15)
sched.start()

db = SQLAlchemy()

    
def register_extensions(app):
    db.init_app(app)
 


def register_blueprints(app):
    for module_name in ('base','admin'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    return app