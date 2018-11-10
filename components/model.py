from datetime import datetime
from components.protected_list import ProtectedList
from components.enumm import Enum

implicit_converter = {#str: lambda value: str(value),
                      #int: lambda value: int(value),
                      #bool: lambda value: str(value).lower() in [1, 'true', 'y'],
                      datetime: lambda value: datetime.strptime(value, '%b %d %Y %I:%M%p')} # 'Jun 1 2005  1:33PM'

class Model(type):
    def init(self, **kwargs):
        # If we have any kwargs, try and set them if they fit the definitions
        for key, value in kwargs.items():
            if key in self.descriptors:
                self.__setattr__(key, value)

    def __new__(cls, name, bases, dct):
        # Get all the descriptors for this class from the annotations and parent annotations
        base_annotations = {key: cls.parse_annotation_value(value) for base in bases for key, value in base.__dict__.get('__annotations__').items()}
        cls_annotations = {key: cls.parse_annotation_value(value) for key, value in dct.get('__annotations__').items()}
        annotations = {**cls_annotations, **base_annotations}

        dct.update({
            'descriptors': annotations,
            '__setattr__': cls.strict_set,
            '__getattr__': cls.__getattr__,
            '__init__': cls.init,
            'serialise': cls.serialise,
            '__str__': lambda self: str(self.serialise())
        })

        # Create a new class
        x = super().__new__(cls, name, bases, dct)
        return x

    def serialise(self):
        serialised = {}

        for key in self.__dict__:
            print("Serialising {}".format(key))
            definition = self.descriptors[key]

            if ProtectedList in definition.__bases__:
                print("Is a protected list {}".format(self.__dict__[key][0]))
                print(definition.__bases__)
                serialised[key] = [value.serialise() if isinstance(value, Model) else value for value in self.__dict__[key]]

            elif Enum in definition.__bases__:
                serialised[key] = self.__dict__[key].serialise() if isinstance(self.__dict__[key], Model) else self.__dict__[key]

            elif definition in [int, str, datetime, bool, dict]:
                serialised[key] = self.__dict__[key]

            elif Model in definition.__bases__:
                serialised[key] = self.__dict__[key].serialise()

        return serialised

    def __getattr__(self, key):
        """
        We will get by key, looking at the instance dict first, then the descriptors, and if the descriptor is for a protected list,
        we will instanciate it
        """
        # If the value has been instanciated
        if key in self.__dict__:
            return self.__dict__.get(key)

        if key in self.descriptors:
            definition = self.descriptors.get(key)
            # If it is a ProtectedList, we will instanciate it
            if ProtectedList in definition.__bases__:
                self.__dict__[key] = definition()
                return self.__dict__.get(key)
        else:
            raise KeyError("Key {} not found in annotations".format(key))


    @classmethod
    def parse_annotation_value(cls, value):
        """
        Convert the annotation from a type or instance, into a type
        """
        # Value is either a type, or an instance that needs turning into a type
        if isinstance(value, type):
            return value

        elif isinstance(value, list):
            assert type(value[0]) == type or type(type(value[0])) == type
            return ProtectedList.of(value[0])

        elif isinstance(value, tuple):
            return Enum.of(*value)

        else:
            raise TypeError("Unable to parse annotation value {}".format(value))

    def strict_set(self, key, value):
        definition = self.descriptors[key]

        if not isinstance(value, definition):
            # We will try to convert it to the correct type
            if definition in implicit_converter:
                try:
                    value = implicit_converter[definition](value)
                    return setattr(self, key, value)
                except:
                    # Failed to convert the value. Either return or raise
                    pass

            # When setting a protected list, it might be passed to us as a list, so we turn it into a protected list
            elif ProtectedList in definition.__bases__ and isinstance(value, list):
                protected_list = definition()
                protected_list.extend(value)
                return setattr(self, key, protected_list)

            elif Enum in definition.__bases__:
                self.__dict__[key] = definition.validate(value)
                return

            raise ValueError("Key {} requires value type {} received type {}".format(
                key,
                definition,
                type(value)
            ))


        self.__dict__[key] = value
        return

