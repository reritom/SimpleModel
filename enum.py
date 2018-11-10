class Enum():
    @classmethod
    def of(cls, definitions):
        return type(cls.__name__ + '_'.join([definition.__name__ for definition in definitions]),
                    (cls,),
                    {'definitions': definitions})

    @classmethod
    def validate(cls, value):
        return type(value) in cls.definitions