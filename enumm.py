class Enum():
    @classmethod
    def of(cls, definitions):
        return type(cls.__name__ + '_'.join([definition.__name__ for definition in definitions]),
                    (cls,),
                    {'definitions': definitions})

    @classmethod
    def validate(cls, value):
        if not type(value) in cls.definitions:
            raise TypeError("Value of type {} does not fit in Enum definitions {}".format(
                type(value),
                cls.definitions
            ))
        return value