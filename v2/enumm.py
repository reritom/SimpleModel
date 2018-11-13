class Enum():
    @classmethod
    def of(cls, *definitions):
        # An enum can be of a mixture of types or instances
        defs = []
        print("Enum defs are {}".format(definitions))

        for definition in definitions:
            if isinstance(definition, type):
                # This is a class, take the name
                defs.append(definition.__name__)
            else:
                defs.append("instanceOf_{}".format(definition.__class__.__name__))

        return type(cls.__name__ + '_' + '_'.join(defs),
                    (cls,),
                    {'definitions': definitions})

    @classmethod
    def validate(cls, value):
        print("Validating value {}".format(value))
        if type(value) in cls.definitions or value in cls.definitions:
            return value

        raise ValueError("Value {} does not fit in Enum definitions {}".format(
            value,
            cls.definitions
        ))