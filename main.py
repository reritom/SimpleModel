from sample_model import User, Business# Ticket

user = User()
print("User descriptors {}".format(user.descriptors))

business = Business()
print("Business descriptors {}".format(business.descriptors))

business.serialise()