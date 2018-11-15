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
            print("This is ok")
            return value

        # We might be trying to validate a serialised input, which means deserialising it
        try:
            print("Trying to deserialise it")
            value = cls.deserialise(value)
            return value
        except:
            pass

        raise ValueError("Value {} does not fit in Enum definitions {}".format(
            value,
            cls.definitions
        ))

    @classmethod
    def serialise(cls, value):
        return {value.__class__.__name__: value}

    @classmethod
    def deserialise(cls, value):
        assert isinstance(value, dict), "Deserialising enum requires dict, got {}".format(type(value))
        # Value is a string of a classname
        class_name = list(value.keys())[0]
        enum_class_index = [def_class.__name__ if hasattr(def_class, '__name__') else def_class.__class__.__name__ for def_class in cls.definitions].index(class_name)
        enum_class = cls.definitions[enum_class_index]

        if hasattr(enum_class, 'deserialise'):
            return enum_class.deserialise(value[class_name])
        else:
            return value[class_name]