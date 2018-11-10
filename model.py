from datetime import datetime
from protected_list import ProtectedList
from enum import Enum

implicit_converter = {str: lambda value: str(value),
                      int: lambda value: int(value),
                      bool: lambda value: str(value).lower() in [1, 'true', 'y'],
                      datetime: lambda value: datetime.strptime(value, '%b %d %Y %I:%M%p')} # 'Jun 1 2005  1:33PM'

class Model(type):
    def __new__(cls, name, bases, dct):
        # Get all the descriptors for this class from the annotations and parent annotations
        base_annotations = {key: cls.parse_annotation_value(value) for base in bases for key, value in base.__dict__.get('__annotations__').items()}
        cls_annotations = {key: cls.parse_annotation_value(value) for key, value in dct.get('__annotations__').items()}
        annotations = {**cls_annotations, **base_annotations}

        dct.update({
            'descriptors': annotations,
            'serialise': cls.serialise,
            '__setattr__': lambda self, key, value: cls.strict_set(self, key, value, self.descriptors[key]),
            '__getattr__': lambda self, key: self.__dict__.get(key) or self.descriptors.get(key)
        })

        # Create a new class
        x = super().__new__(cls, name, bases, dct)
        return x

    @classmethod
    def parse_annotation_value(cls, value):
        # Value is either a type, or an instance that needs turning into a type
        if isinstance(value, type):
            return value

        elif isinstance(value, list):
            assert type(value[0]) == type
            return ProtectedList.of(value[0])

        elif isinstance(value, tuple):
            return Enum.of(list(value))

        else:
            raise TypeError("Unable to parse annotation value {}".format(value))

    def strict_set(self, key, value, definition):
        if not isinstance(value, definition):
            # We will try to convert it to the correct type
            if definition in implicit_converter:
                try:
                    value = implicit_converter[definition](value)
                    return setattr(self, key, value)
                except:
                    # Failed to convert the value. Either return or raise
                    pass

            raise ValueError("Key {} requires value type {} received type {}".format(
                key,
                definition,
                type(value)
            ))

        self.__dict__[key] = value
        return

