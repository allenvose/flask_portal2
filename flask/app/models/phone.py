from datetime import (datetime, timezone)
import pytz
import phonenumbers
import requests
from twilio.rest import Client
from twilio.rest.verify.v2.service import verification
from phonenumbers import NumberParseException, PhoneNumber, carrier, timezone, PhoneNumberMatcher, geocoder, geodata
from py2neo.ogm import Model, Repository
from py2neo.ogm import  Node, Label,  Property, Related, RelatedTo, RelatedFrom
from app import db


class Person(Model):
    __primarylabel__ = 'Person'
    __primarykey__ = 'first_name'

    first_name = Property()
    last_name = Property()
    middle_name = Property()
    title = Property()
    birth_day = Property()
    image = Property()

    system_accounts = RelatedTo('System_Account')
    employed_by = RelatedTo('Company')
    phone_numbers = RelatedTo('Phone')
    
    def fetch(self, _id):
        return Person.match(db.repo, _id).first()
    
    def fetch_by_first_and_last(self):
        return Person.match(db.repo).where(
            f'_.first_name = "{self.first_name}" AND _.last_name = "{self.last_name}"'
        ).first()
    
    @classmethod
    def create_new(cls, first_name, last_name, middle_name=None, title=None, birth_day=None, image=None):
        return cls(first_name=first_name, last_name=last_name, middle_name=middle_name,
                    title=title, birth_day=birth_day, image=image)

    def save(self):
        db.repo.save(self)

class Phone(Model):
    __primarylabel__ = 'Phone'
    __primarykey__ = "phone_number"

    phone_number = Property()
    national_format = Property()
    international_format= Property()
    e164_format = Property()
    likely_region = Property()
    get_timezone = Property()
    likely_timezone = Property()
    likely_carrier = Property()
    line_type = Property()
    shared_line = Property()
    personal_line = Property()
    company_line = Property()
    is_validated = Property()

    users = RelatedFrom('Person', 'PHONE_NUMBERS') 

    def get(self):
        return self.match(db.repo, self.phone_number).first()
    
    def exists(self):
        check = self.get()
        if check:
            return True
        return False
    
    def save(self):
        db.repo.save(self)
    
    @classmethod
    def create_new(cls, new_phone_number, shared_line=None, personal_line=None, company_line=None):
        phone_number = phonenumbers.parse(new_phone_number)
        is_possible = phonenumbers.is_possible_number(phone_number)
        is_valid = phonenumbers.is_valid_number(phone_number)
        if is_possible is True and is_valid is True:
            is_validated = True
            national_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            international_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            e164_format = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164 )
            likely_carrier = str(Phone.get_carrier(e164_format))
            likely_region = geocoder.description_for_number(phone_number, 'en')
            likely_timezone =  timezone.time_zones_for_number(phone_number)
            line_type =  MobileVerification(e164_format).line_type()
            is_shared_line = shared_line
            is_personal_line = personal_line
            is_company_line = company_line
            return cls(phone_number=e164_format, national_format=national_format, international_format=international_format,
                        e164_format=e164_format, likely_region=likely_region, likely_timezone=likely_timezone,
                    likely_carrier=likely_carrier, line_type=line_type, is_shared_line=is_shared_line,
                    is_personal_line=is_personal_line, is_company_line=is_company_line, is_validated=is_validated)
        
    @staticmethod
    def get_carrier(phone_number):
        try:
            response = requests.get('https://api.telnyx.com/v1/phone_number/'+phone_number, timeout=5)
            #response.raise_for_status()
            data = response.json()
            # Code here will only run if the request is successful
        except requests.exceptions.HTTPError:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.RequestException:
            return None
                
        return data["carrier"]["name"]
      
class MobileVerification():
    
    def __init__(self, phone_number):    
        self._account_sid = 'AC246cd0573516203969002ce2c74cbda2'
        self._auth_token = '8f865be3fc21aa8ce18a7c812496c24d'
        self._client = Client(self._account_sid, self._auth_token)
        self.phone = phone_number

    def sms_verification_create(self):
        verification_request = self._client.verify \
            .services('VA58eb41ac7cb456186ed2847e83914a35') \
            .verifications \
            .create(to=self.phone, channel='sms')
        print(verification_request.status)
        return verification_request

    def sms_verification_check(self, code):
        """
        Args:
            code (string): verification code sent to mobile
        Returns:
            dict : record with verification status
            values  include status, to, date_created, status, channel
        """
        verification_status = self._client.verify \
            .services('VA58eb41ac7cb456186ed2847e83914a35') \
            .verification_checks \
            .create(to=self.phone, code=code)
        print(verification_status.status)
        return verification_status
        
    def line_type(self):
        """
        Args:
            phone_number (string): phone number in e.164 format
        Returns:
            string: line type associated with the phone number
            possible values are mobile, landline, or voip
        """
        phone_number_type = self._client \
            .lookups \
            .phone_numbers(self.phone) \
            .fetch(type='carrier') \
            .carrier

        return phone_number_type['type']

    def twilio_create_verify_service(service_name):
        account_sid = 'AC246cd0573516203969002ce2c74cbda2'
        auth_token = '8f865be3fc21aa8ce18a7c812496c24d'
        client = Client(account_sid, auth_token)
        service = client.verify.services.create(
                friendly_name=service_name)
        return service.sid

# def start():
#     phone = Phone('7038194577')
#     phone.print()
#     #phone.send_sms_verification()
#     phone.check_sms_verification_response('631246  ')
#     #twilio = Twilio_Service('+17038194577')
#     #print(dir(twilio.sms_verification_create()))
#     #twilio.sms_verification_check('4446')

def start():
    phone_number = Phone('15735879635')
    

if __name__ == '__main__':
    start()
            