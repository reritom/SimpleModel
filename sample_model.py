from model import Model
from datetime import datetime

class Ticket(metaclass=Model):
    number: str
    holder: str
    created: datetime
    options: dict

class User(metaclass=Model):
    name: str
    email: str
    aliases: [str]

class Card(metaclass=Model):
    vendor: str
    code: str

class Cash(metaclass=Model):
    code: str

class Business(User, metaclass=Model):
    business_name: str
    business_id: str
    description: str
    accepted_payments: (Card, Cash,)

    def logic(self):
        print("logic")

class Holder(User, metaclass=Model):
    holder_id: str


