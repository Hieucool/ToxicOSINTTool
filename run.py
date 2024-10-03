# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from flask_migrate import Migrate
from os import environ
from sys import exit
from config import config_dict

from app import create_app, db



try:

    app_config = config_dict['Debug']

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
    

app = create_app(app_config) 
# Migrate(app, db)


if __name__ == "__main__":
    
    app.run()