from protected_list import ProtectedList
from enumm import Enum
from descriptor import Descriptor

class Model:
    def __new__(cls, *args, **kwargs):
        print("In new")
        base_annotations = {}
        for base in reversed(cls.__bases__):
            print("Looking at base {}".format(base.__name__))
            base_annotations.update(getattr(base, '__annotations__', {}))

        base_annotations = {key: parse_annotation_value(value) for key, value in base_annotations.items()}
        print("Base annotations {}".format(base_annotations))
        class_annotations = {key: parse_annotation_value(value) for key, value in cls.__annotations__.items()}
        print("Class annotations {}".format(class_annotations))
        annotations = {**base_annotations, **class_annotations}

        print("New annotations are {}".format(annotations))

        # Validate that the default values match the annotations
        for key in annotations:
            if key in cls.__dict__:
                print("{} has a default value".format(key))
                # A default value has been set
                annotations[key].validate(cls.__dict__[key])

        setattr(cls, 'descriptors', annotations)

        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            print("Kwarg is {}".format(key))
            if key in self.descriptors:
                print("{} is in descriptors".format(key))
                setattr(self, key, value)

        # Set any of the default values
        for key in self.descriptors:
            print("Init {}".format(key))
            if key in self.__class__.__dict__:
                print("Key {} has default value {} trying to set it".format(key, self.__class__.__dict__[key]))
                setattr(self, key, self.__class__.__dict__.get(key))

        print("Dict after init is {}".format(self.__dict__))

    def serialise(self):
        serialised = {}
        for key, value in self.__dict__.items():
            if hasattr(value, 'serialise'):
                # ProtectedList or nested Model
                serialised[key] = value.serialise()
            elif Enum in self.descriptors[key].__bases__:
                pass
            else:
                serialised[key] = value

        return serialised

    def deserialise(self):
        pass


    def __getattr__(self, key):
        print("Getting attribute {}".format(key))

        if key in self.descriptors and key not in self.__dict__ and ProtectedList in self.descriptors[key].__bases__:
            self.__dict__[key] = self.descriptors[key]()
            return self.__dict__[key]

        return self.__dict__[key]


    def __setattr__(self, key, value):
        print("Descriptors are {}".format(self.descriptors))

        if not key in self.descriptors:
            raise KeyError()

        self.descriptors[key].validate(value)
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
    print("Model class bases are{} {}".format(cls, cls.__bases__))
    bases = (cls,) + cls.__bases__ if Model in cls.__bases__ else (cls,) + cls.__bases__[:-1] + (Model, object,)
    print("Bases are {}".format(bases))
    return type(cls.__name__, bases, {**cls.__dict__, **Model.__dict__}) #{'descriptors': {**class_annotations, **base_annotations}})

