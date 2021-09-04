"""
"""
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.blueprints.base import blueprint
from app.blueprints.auth.forms import LoginForm 
from app.models.auth import System_Account
from app.blueprints.base.util import verify_pass
from app import db, login_manager


@blueprint.route('/')
def route_default():
    return redirect(url_for('auth_blueprint.login'))


@blueprint.route('/create/<string:name>')
def create(name):
    db.graph.run("CREATE (n:User {name: '%s'})" % name) # noqa
    return jsonify('user %s created' % name)




# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
