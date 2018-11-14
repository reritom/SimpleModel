class Descriptor:
    @classmethod
    def of(cls, definition):
        return type(cls.__name__ + '_' + definition.__name__,
                    (cls,),
                    {'definition': definition})

    @classmethod
    def validate(cls, value):
        if not isinstance(value, cls.definition):
            raise ValueError("Setting invalid type {} to descriptor of {} with value {}".format(
                type(value),
                cls.definition,
                value
            ))
        return value

    @classmethod
    def serialise(self, value):
        if hasattr(value, 'serialise'):
            return value.serialise()

        return value

    @classmethod
    def deserialise(cls, value):
        if hasattr(cls.definition, 'deserialise'):
            return cls.definition.deserialise(value)

        return value
