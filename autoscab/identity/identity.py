import typing
from pathlib import Path
import random

import requests
from faker import Faker

from autoscab.identity.resume import make_resume
from autoscab.constants.agents import USER_AGENTS
from autoscab.utils import random_email

MAIL_SERVICES = typing.Literal['guerilla', 'mailtm']

class Identity:
    def __init__(self, email_service:MAIL_SERVICES = 'guerilla'):
        self.email_service = email_service

        self.faker = Faker()

        self.name = self.get_name()
        self.password = self.get_password()
        self.ssn = self.faker.ssn()
        phone = ''
        while len(phone)<1 or len(phone)>12:
            phone = self.faker.phone_number()
        self.phone = phone
        self.address = self.faker.street_address()
        self.city = self.faker.city()
        self.state = self.faker.state()
        self.zip = self.faker.zipcode()


        self.user_agent = random.choice(USER_AGENTS)

        email = self.get_email(self.email_service)
        self.email = email['email']
        self.email_sid = email['sid']

        self.resume = self.get_resume()




    def get_name(self) -> typing.List[str]:
        return [self.faker.first_name(), self.faker.last_name()]

    def get_email(self, service:typing.Literal['guerilla', 'mailtm']='guerilla') -> typing.Dict[str,str]:
        if service == 'guerilla':
            response = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address').json()
            fake_email = response.get('email_addr')
            mail_sid = response.get('sid_token')
        elif service == 'mailtm':
            fake_email = requests.post('https://api.mail.tm/accounts', data='{"address":"' + random_email(
                self.name[0] + ' ' + self.name[1]) + '","password":" "}',
                                       headers={'Content-Type': 'application/json'}).json().get('address')
            mail_sid = requests.post('https://api.mail.tm/token',
                                     data='{"address":"' + fake_email + '","password":" "}',
                                     headers={'Content-Type': 'application/json'}).json().get('token')
        else:
            raise ValueError('Dont know what email service to use! try one of guerilla or mailtm')

        return {'email': fake_email, 'sid': mail_sid}

    def get_password(self) -> str:
        return self.faker.password()

    def get_resume(self) -> Path:
        return make_resume(
            name = " ".join(self.name),
            email = self.email
        )