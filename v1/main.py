from sample_model import User, Business, Hotel# Ticket
from components.model import Model
'''
user = User()
print("User descriptors {}".format(user.descriptors))

business = Business()
print("Business descriptors {}".format(business.descriptors))

#business.business_name = "Chilli"
business.name = "test"
print(business.business_name)
business.logic()
print(business.__dict__)

#print(business.aliases)
#business.aliases.append("Hi")
print(business.__dict__)
'''
new_business = Business(name="Hello", aliases=[Hotel(code="Artemis")])
print("Business is instance {}".format(isinstance(new_business, Business)))
new_business.business_type = Hotel(code="Windsor")
print("New business is {}".format(new_business))
new_business.business_type = 1
print(new_business.business_type)
