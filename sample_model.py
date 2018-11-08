from model import Model

from datetime import datetime

'''
class Ticket(metaclass=Model):
    number: str
    holder: str
    created: datetime
    options: dict

'''
class User(metaclass=Model):
    name: str
    email: str

class Business(User, metaclass=Model):
    business_name: str
    business_id: str
    description: str
'''
class Holder(User, metaclass=Model):
    holder_id: str
'''

