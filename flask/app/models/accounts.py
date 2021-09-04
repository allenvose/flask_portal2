from passlib.hash import sha256_crypt
from py2neo.ogm import Model
from py2neo.ogm import  Node, Label,  Property, Related, RelatedTo, RelatedFrom
from app import db
from app.models.person import Person

class System_Account(Model):
    __primarylabel__ = 'System_Account'
    __primarykey__ = "username"

    username = Property()
    email = Property()
    hashed_password =Property()
    is_active = Label() 

    user_account = RelatedFrom('Person', 'USER_ACCOUNT') 

    def get_id(self):         
        return str(self.username)
   
    def is_active(self):   
        return True  

    def verify_password(self, input_password):
        return sha256_crypt.verify(input_password, self.hashed_password)


    def __repr__(self):
        return str(self.username)
