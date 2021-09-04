import re
from passlib.hash import sha256_crypt
from wtforms import ValidationError
import phonenumbers
from phonenumbers import NumberParseException
from app import db
from app.models.phone import Phone
from app.models.accounts import System_Account


def hash_password(password_input):
    return sha256_crypt.encrypt(password_input)


def sms_field_validator():
    def _new_sms_number(form, field):
                try:
                    sms_capable_phone = field.data.replace(' ', '')
                    sms_capable_phone = sms_capable_phone.replace('-', '')
                    sms_capable_phone = sms_capable_phone.replace('(', '')
                    sms_capable_phone = sms_capable_phone.replace(')', '')
                    if len(sms_capable_phone) == 10:
                        sms_capable_phone = '1'+sms_capable_phone
                    sms_capable_phone =  '+'+sms_capable_phone
                    sms_capable_phone =  phonenumbers.parse(sms_capable_phone)
                    is_possible = phonenumbers.is_possible_number(sms_capable_phone)
                    is_valid = phonenumbers.is_valid_number(sms_capable_phone)
                    if is_possible is False or is_valid is False:
                        raise ValidationError('This number does not appear to be a valid phone number')
                    field.data = phonenumbers.format_number(sms_capable_phone, phonenumbers.PhoneNumberFormat.E164 )
                except NumberParseException:
                    raise ValidationError('This number does not appear to be a valid phone number')
                try:
                    field.data = phonenumbers.format_number(sms_capable_phone, phonenumbers.PhoneNumberFormat.E164 )
                    if Phone.match(db.repo, field.data).first():
                        raise ValidationError('This number is already registered')
                except:
                    raise ValidationError('There was a problem registering this number')
    return _new_sms_number


def already_exists_validator():
    def __check__(form, field):
        try:
            other = form['company_association']
        except KeyError:
            raise ValidationError(field.gettext(u"Invalid field name company_association."))
        try:
            username = str(field.data + other.data)
            print(username)
            if System_Account.match(db.repo, username).first():
                raise ValidationError('This username is already registered')
        except:
            raise ValidationError('There was a problem registering this number')
    return __check__

    
        
            

            