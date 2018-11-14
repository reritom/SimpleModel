from protected_list import ProtectedList
from enumm import Enum
from descriptor import Descriptor
import inspect
from inspect import Parameter, Signature

class Model:
    def __new__(cls, *args, **kwargs):
        print("In new")
        base_annotations = {}
        for base in reversed(cls.__bases__):
            print("Looking at base {}".format(base.__name__))
            base_annotations.update(getattr(base, '__annotations__', {}))

        base_annotations = {key: parse_annotation_value(value) for key, value in base_annotations.items()}
        class_annotations = {key: parse_annotation_value(value) for key, value in cls.__annotations__.items()}
        annotations = {**base_annotations, **class_annotations}

        #print("New annotations are {}".format(annotations))
        defaults = {attr[0]: attr[1] for attr in inspect.getmembers(cls) if not attr[0].startswith('__') and not callable(attr[1])}
        cls._defaults = defaults

        # Validate that the default values match the annotations
        print("Annotation keys {}".format(annotations.keys()))
        print("Defaults {}".format(defaults.keys()))
        for key in annotations:
            if key in defaults:
                print("{} has a default value {} {}".format(key, defaults[key], annotations[key]))
                # A default value has been set
                annotations[key].validate(defaults[key])

        cls._descriptors = annotations

        # Create the signature
        cls.__signature__ = Signature(parameters=[Parameter(key, Parameter.KEYWORD_ONLY) for key in annotations])

        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print("Initialising")
        for key, value in kwargs.items():
            if key in self._descriptors:
                print("Init arg {}".format(key))
                setattr(self, key, value)

        # Set any of the default values
        for key in self._descriptors:
            if key in self.__class__._defaults:
                print("Key {} has default value {} trying to set it".format(key, self.__class__._defaults[key]))
                setattr(self, key, self.__class__._defaults.get(key))

        print("Dict after init is {}".format(self.__dict__))

    def serialise(self):
        serialised = {}
        for key, value in self.__dict__.items():
            if hasattr(value, 'serialise'):
                # ProtectedList or nested Model
                serialised[key] = value.serialise()
            elif hasattr(self._descriptors[key], 'serialise'):# Enum in self._descriptors[key].__bases__:
                serialised[key] = self._descriptors[key].serialise(value)
            else:
                serialised[key] = value

        return serialised

    @classmethod
    def deserialise(cls, serialised):
        self = cls()
        for key, value in serialised.items():
            if key in self._descriptors:
                print("Attempting to deserialise {}, type is {}".format(key, self._descriptors[key]))
                setattr(self, key, self._descriptors[key].deserialise(value))
        return self


    def __getattr__(self, key):
        print("Getting attribute {}".format(key))

        if key in self._descriptors and key not in self.__dict__ and ProtectedList in self._descriptors[key].__bases__:
            self.__dict__[key] = self._descriptors[key]()
            return self.__dict__[key]

        return self.__dict__[key]


    def __setattr__(self, key, value):
        if not key in self._descriptors:
            raise KeyError()

        value = self._descriptors[key].validate(value)
        return super().__setattr__(key, value)

def parse_annotation_value(value):
    """
    Convert the annotation from a type or instance, into a type
    """
    # Value is either a type, or an instance that needs turning into a type
    if isinstance(value, type):
        return Descriptor.of(value)

    elif isinstance(value, list):
        assert type(value[0]) == type or type(type(value[0])) == type
        return ProtectedList.of(value[0])

    elif isinstance(value, tuple):
        return Enum.of(*value)

    else:
        raise TypeError("Unable to parse annotation value {}".format(value))

def model(cls):
    #class_annotations = {key: parse_annotation_value(value) for key, value in cls.__annotations__.items()}
    #base_annotations = {key: parse_annotation_value(value) for base in cls.__bases__ for key, value in getattr(base, '__annotations__', {}).items()}
    print("Model class bases are {}".format([b for b in cls.__mro__[-1:0:-1]]))
    bases_reverse = [b for b in cls.__mro__[-1:0:-1]]
    if not Model in bases_reverse:
        bases_reverse.insert(1, Model)

    bases = tuple(reversed(bases_reverse))
    return type(cls.__name__, bases, {**cls.__dict__, **Model.__dict__}) #{'descriptors': {**class_annotations, **base_annotations}})

