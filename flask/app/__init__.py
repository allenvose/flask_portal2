"""

"""
from os import path
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from importlib import import_module
from re import A
from flask import Flask, url_for
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from app.extensions.flask_py2neo.driver import Flask_Py2Neo


login_manager = LoginManager()
login_manager.login_view = 'login'
db = Flask_Py2Neo()
principal = Principal()
admin_permission = Permission(RoleNeed("informs_admin"))

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)

def register_blueprints(app):
    for module_name in ('auth', 'base', 'home'):
        module = import_module('app.blueprints.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

# def configure_database(app):

#     # @app.before_first_request
#     # def initialize_database():
#     #     db.create_all()

#     @app.teardown_request
#     def shutdown_session(exception=None):
#         db.session.remove()

def create_app(config):
    app = Flask(__name__, static_folder='base')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    #configure_database(app)
    return app
