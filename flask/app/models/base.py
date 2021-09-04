from passlib.hash import sha256_crypt
from py2neo.ogm import Repository
from py2neo.ogm import GraphObject, Property, Related, RelatedTo, RelatedFrom, Label
from flask_login import UserMixin

from app import db, login_manager
from app.blueprints.base.util import hash_pass

class Neo4jBaseGraph(GraphObject):
    
    
    def save(self):
        if self.account_exists:
            db.graph.merge(self)
            db.graph.push(self)
        else:
            db.graph.create(self)