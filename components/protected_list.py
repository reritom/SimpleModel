class ProtectedList(list):
    @classmethod
    def of(cls, definition):
        return type(cls.__name__ + '_' + definition.__name__,
                    (cls,),
                    {'definition': definition})

    def validate(self, value):
        if not isinstance(value, self.definition):
            raise TypeError("Setting invalid type {} to protected list of {}".format(
                type(value),
                self.definition
            ))
        return value

    def __init__(self, iterator=[]):
        return super().__init__([self.validate(value) for value in iterator])

    def append(self, value):
        return super().append(self.validate(value))

    def insert(self, index, value):
        return super().insert(index, self.validate(value))

    def extend(self, iterator):
        return super().extend([self.validate(value) for value in iterator])