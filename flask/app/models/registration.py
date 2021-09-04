
from datetime import (datetime, timezone)
from dataclasses import dataclass, field
from passlib.hash import sha256_crypt
from py2neo.ogm import Repository
from py2neo.ogm import GraphObject, Property, Related, RelatedTo, RelatedFrom, Label
from flask_wtf import FlaskForm
from phonenumbers import NumberParseException, PhoneNumber, carrier, timezone, PhoneNumberMatcher, geocoder, geodata
from wtforms import PasswordField, StringField, SelectField, Form
from wtforms.validators import InputRequired, Email, DataRequired, Length, Regexp, ValidationError, EqualTo

from app import db
from app.models.phone import Phone, Person
from app.utils.custom_validators import hash_password




class RegistrationSystem(): 
    username: str = None
    password: str = None
    first_name: str = None
    middle_name: str = None
    last_name: str= None
    company_association: str = None
    title: str = None
    sms_capable_phone: str = None
    
    def save(self):
        new_person = Person.create_new(self.first_name, self.last_name)
        new_phone = Phone.create_new(self.sms_capable_phone)
        new_person.phone_numbers.add(new_phone)
        db.repo.save(new_person)
       
        #new_person.save()
        #new_phone.save()



