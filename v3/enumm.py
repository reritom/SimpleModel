class Enum():
    @classmethod
    def of(cls, *definitions):
        self = cls()
        self.definitions = definitions
        return self

    def validate(self, value):
        print("Validating value {}".format(value))
        if type(value) in self.definitions or value in self.definitions:
            print("This is ok")
            return value

        # We might be trying to validate a serialised input, which means deserialising it
        try:
            print("Trying to deserialise it")
            value = self.deserialise(value)
            return value
        except:
            pass

        raise ValueError("Value {} does not fit in Enum definitions {}".format(
            value,
            self.definitions
        ))

    def serialise(self, value):
        return {value.__class__.__name__: value}

    def deserialise(self, value):
        assert isinstance(value, dict), "Deserialising enum requires dict, got {}".format(type(value))
        # Value is a string of a classname
        class_name = list(value.keys())[0]

        enum_class_index = [
            def_class.__name__
            if hasattr(def_class, '__name__')
            else def_class.__class__.__name__
            for def_class in self.definitions].index(class_name)

        enum_class = self.definitions[enum_class_index]

        if hasattr(enum_class, 'deserialise'):
            return enum_class.deserialise(value[class_name])
        else:
            return value[class_name]