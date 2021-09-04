from passlib.hash import sha256_crypt
from py2neo.ogm import Repository
from py2neo.ogm import Model, Property, Related, RelatedTo, RelatedFrom, Label
from flask_login import UserMixin

from app import db, login_manager
from app.blueprints.base.util import hash_pass

class Neo4jBaseGraph():
    @property
    def person_exists(self):
        return db.graph.exists(self)
    
    def save(self):
        if self.account_exists:
            db.graph.merge(self)
            db.graph.push(self)
        else:
            db.graph.create(self)


class Person(Model):
    __primarylabel__ = 'Person'
    __primarykey__ = "username"

    first_name = Property()
    last_name = Property()
    title = Property()
    image = Property()

    has_system_account = Related('System_Account')
    employed_by = Related('Company')

class PhoneNumber(Model):
    __primarylabel__ = 'Phone'
    __primarykey__ = "number"
    pass

class Address(Model):
    pass

class Company(Model):
    pass


class Account_Status(Model):
    pass

class System_Account(Model):
    __primarylabel__ = 'System_Account'
    __primarykey__ = "username"

    username = Property()
    email = Property()
    hashed_password =Property()
    is_active = Label() 

    belongs_to = Related('Person') 

    def get_id(self):         
        return str(self.username)
   
    def is_active(self):   
        return True  

    def verify_password(self, input_password):
        return sha256_crypt.verify(input_password, self.hashed_password)


    def __repr__(self):
        return str(self.username)

@login_manager.user_loader
def user_loader(username):
    return System_Account.match(db.graph, username).first()
    

# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = User.match(db.graph, username).first()
#     return user if user else None


