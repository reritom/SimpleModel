class ProtectedList(list):
    @classmethod
    def of(cls, definition):
        return cls(definition=definition)

    def validate(self, value):
        if isinstance(value, list):
            return self.__class__(iterator=value, definition=self.definition)

        if not isinstance(value, self.definition):
            raise ValueError("Setting invalid type {} to protected list of {}".format(
                type(value),
                self.definition
            ))

        if hasattr(self.definition, 'deserialise'):
            # If we are validating the input from a serialised model, we will need to set a list of serialised components,
            # which means we might need to attempt to deserialise it first
            try:
                value = self.definition.deserialise(value)
                return value
            except:
                pass

        return value

    def validate_set(self, value):
        if not isinstance(value, list):
            raise ValueError("Setting invalid type {} to protected list of {}".format(
                type(value),
                self.definition
            ))

        return self.__class__(iterator=value, definition=self.definition)

    def deserialise(self, value):
        if hasattr(self.definition, 'deserialise'):
            value = [self.definition.deserialise(elem) for elem in value]

        return self.__class__(iterator=value, definition=self.definition)

    def serialise(self):
        serialised = []

        for value in self[:]:
            if hasattr(value, 'serialise'):
                serialised.append(value.serialise())
            else:
                serialised.append(value)

        return serialised

    def copy(self):
        return self.__class__(definition=self.definition)

    def __init__(self, definition=None, iterator=[]):
        if definition:
            self.definition = definition

        return super().__init__([self.validate(value) for value in iterator])

    def append(self, value):
        return super().append(self.validate(value))

    def insert(self, index, value):
        return super().insert(index, self.validate(value))

    def extend(self, iterator):
        return super().extend([self.validate(value) for value in iterator])