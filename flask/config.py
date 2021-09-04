# -*- encoding: utf-8 -*-
"""

"""

import os
from   decouple import config

class Config(object):

    #SETUP Flask Base Enviroment Variables and Defaults
    BASEDIR  = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
   

class ProductionConfig(Config):
    
    #Production Mode turn off flask debug and set cookie security
    DEBUG = False
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
    

class DebugConfig(Config):
    #Debug/Development Mode turn on flask debug
    DEBUG = True
    #NEO4J_URI = 'http://neo4j:7474'
    NEO4J_PASSWORD = 'test'
    NEO4J_USER = 'neo4j'
    NEO4J_HOST = 'neo4j'


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
