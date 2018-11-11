from components.model import Model
from datetime import datetime
'''
class Ticket(Model):
    number: str
    holder: str
    created: datetime
    options: dict
'''
class User(Model):
    name: str
    email: str

class Hotel(Model):
    vendor: str
    code: str

class Shop(Model):
    code: str

class Business(User):
    business_name: str
    business_id: str
    description: str
    business_type: (Hotel, Shop,)
    aliases: [Hotel]

    def logic(self):
        print("Business is {}".format(self.business_name))
'''
class Holder(User):
    holder_id: str
'''

