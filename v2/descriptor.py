class Descriptor:
    @classmethod
    def of(cls, definition):
        return type(cls.__name__ + '_' + definition.__name__,
                    (cls,),
                    {'definition': definition})

    @classmethod
    def validate(cls, value):
        if not isinstance(value, cls.definition):
            raise ValueError("Setting invalid type {} to protected list of {}".format(
                type(value),
                cls.definition
            ))
        return value
