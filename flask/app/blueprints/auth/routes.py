
from passlib.hash import sha256_crypt

from flask import current_app, jsonify, render_template, redirect, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_principal import (
    AnonymousIdentity, Identity, Principal, RoleNeed, UserNeed,
    identity_changed, identity_loaded,)

from app.blueprints.auth import blueprint
from app.blueprints.auth.forms import RegistrationForm, LoginForm
from app.models.registration import RegistrationSystem
from app.models.auth import System_Account
from app.blueprints.base.util import verify_pass
from app import db, login_manager, admin_permission

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        #user = System_Account.match(db.graph, request.form['username']).first()
        user = db.repo.match(System_Account, request.form['username']).first()
        if user:
            if user.verify_password(request.form['password']) is True:
                login_user(user)
                identity_changed.send(
                    current_app._get_current_object(), identity=Identity(user.user))
                return redirect(url_for('base_blueprint.route_default'))
            if user.verify_password(request.form['password']) is False:
                return render_template( 'accounts/login.html',
                                        msg='Wrong username or password',
                                         form=login_form)
        if user is None:
            return render_template( 'accounts/login.html',
                                        msg='Wrong username or password',
                                         form=login_form)
    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form, segment='index')
    return redirect(url_for('home_blueprint.index'))



@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm(request.form)
    if 'register' in request.form:
        if registration_form.validate_on_submit():
            registration_form.password.data = sha256_crypt.encrypt(registration_form.password.data)
            new_user = RegistrationSystem()
            registration_form.populate_obj(new_user)
            print(new_user)
            new_user.save()
            #test_model = CreateAccountModel.from_orm(create_account_form)
            #print(test_model)
            # system_account = db.repo.match(System_Account, create_account_form.username).first()
            # mobile_phone = db.repo.match(Phone, create_account_form.sms_number).first()
            # if system_account:
            #     if system_account.username == create_account_form.username:
            #         return render_template( 'accounts/register.html', 
            #                             msg='Username already registered, please login or request help',
            #                             success=False,
            #                             form=create_account_form)
            #     if system_account.email == create_account_form.email:
            #         return render_template( 'accounts/register.html', 
            #                             msg='Email already registered, please login or request help', 
            #                             success=False,
            #                             form=create_account_form)
            # if mobile_phone:
            #     if mobile_phone.phone_number == create_account_form.sms_number:
            #         return render_template( 'accounts/register.html', 
            #                             msg='Mobile number is already registered',
            #                             success=False,
            #                             form=create_account_form)

            # if system_account is None and mobile_phone is None:
            # # # else we can create the user
            #     hashed_pasword = sha256_crypt.encrypt(create_account_form.password)
            #     system_account = System_Account()
            #     system_account.username = username
            #     system_account.email = email
            #     system_account.hashed_password = hashed_pasword
            #     db.repo.save(system_account)
            #     print('User Created')
            #     return render_template( 'accounts/register.html', 
            #                     msg='User created please <a href="/login">login</a>', 
            #                     success=True,
            #                     form=create_account_form)
        # else:
        #     return render_template( 'accounts/login.html',
        #                             form=create_account_form,
        #                             success=False, segment='index')
   
    return render_template( 'accounts/register.html', form=registration_form, segment='index')


@blueprint.route('/logout')
def logout():
    logout_user()
    for key in ("identity.name", "identity.auth_type"):
        session.pop(key, None)
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('auth_blueprint.login'))

@blueprint.route('/admin_test')
@admin_permission.require(http_exception=404)
def admin_test():
    return 'Admin Test'