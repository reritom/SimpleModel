from components.model import Model
from datetime import datetime

class Ticket(metaclass=Model):
    number: str
    holder: str
    created: datetime
    options: dict

class User(metaclass=Model):
    name: str
    email: str

class Hotel(metaclass=Model):
    vendor: str
    code: str

class Shop(metaclass=Model):
    code: str

class Business(User, metaclass=Model):
    business_name: str
    business_id: str
    description: str
    business_type: (Hotel, Shop,)
    aliases: [Hotel]

    def logic(self):
        print("Business is {}".format(self.business_name))

class Holder(User, metaclass=Model):
    holder_id: str


