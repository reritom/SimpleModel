from sample_model import User, Business# Ticket

user = User()
print("User descriptors {}".format(user.descriptors))

business = Business()
print("Business descriptors {}".format(business.descriptors))

business.business_name = "Chilli"
business.name = "test"
print(business.business_name)
business.logic()
print(business.__dict__)
print(business.__class__.__dict__)

