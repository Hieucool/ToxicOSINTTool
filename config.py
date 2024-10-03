import os

class Config(object):
    basedir    = os.path.abspath(os.path.dirname(__file__))
    # This will create a file in <app> FOLDER
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'osintnews.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class DebugConfig(Config):
    DEBUG = True
    
config_dict = {
    'Debug'     : DebugConfig
}