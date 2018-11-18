class Descriptor:
    @classmethod
    def of(cls, definition):
        self = cls()
        self.definition = definition
        return self

    def validate(self, value):
        if not isinstance(value, self.definition):
            raise ValueError("Setting invalid type {} to descriptor of {} with value {}".format(
                type(value),
                self.definition,
                value
            ))
        return value

    def serialise(self, value):
        if hasattr(value, 'serialise'):
            return value.serialise()

        return value

    def deserialise(self, value):
        if hasattr(self.definition, 'deserialise'):
            return self.definition.deserialise(value)

        return value
