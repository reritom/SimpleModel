class ProtectedList(list):
    @classmethod
    def of(cls, definition):
        return type(cls.__name__ + '_' + definition.__name__,
                    (cls,),
                    {'definition': definition})

    @classmethod
    def validate(cls, value):
        if isinstance(value, list):
            return cls(value)

        if not isinstance(value, cls.definition):
            raise ValueError("Setting invalid type {} to protected list of {}".format(
                type(value),
                cls.definition
            ))

        if hasattr(cls.definition, 'deserialise'):
            # If we are validating the input from a serialised model, we will need to set a list of serialised components,
            # which means we might need to attempt to deserialise it first
            try:
                value = cls.definition.deserialise(value)
                return value
            except:
                pass

        return value

    @classmethod
    def validate_set(cls, value):
        if not isinstance(value, list):
            raise ValueError("Setting invalid type {} to protected list of {}".format(
                type(value),
                cls.definition
            ))

        return cls(value)

    @classmethod
    def deserialise(cls, value):
        if hasattr(cls.definition, 'deserialise'):
            print("DESE {} {}".format(value, cls.definition))
            value = [cls.definition.deserialise(elem) for elem in value]

        return cls(value)

    def serialise(self):
        serialised = []

        for value in self[:]:
            if hasattr(value, 'serialise'):
                serialised.append(value.serialise())
            else:
                serialised.append(value)

        return serialised

    def __init__(self, iterator=[]):
        return super().__init__([self.validate(value) for value in iterator])

    def append(self, value):
        return super().append(self.validate(value))

    def insert(self, index, value):
        return super().insert(index, self.validate(value))

    def extend(self, iterator):
        return super().extend([self.validate(value) for value in iterator])