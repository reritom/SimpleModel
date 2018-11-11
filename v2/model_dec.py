from protected_list import ProtectedList
from enumm import Enum

class Model:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if key in self.descriptors:
                setattr(self, key, value)

    def serialise(self):
        pass

    def deserialise(self):
        pass

    def __getattr__(self, key):
        print("Getting {}".format(key))
        print(key in self.descriptors)
        print(key not in self.__dict__)
        print(ProtectedList in self.descriptors[key].__bases__)
        if key in self.descriptors and key not in self.__dict__ and ProtectedList in self.descriptors[key].__bases__:
            self.__dict__[key] = self.descriptors[key]()
            return getattr(self, key)


    def __setattr__(self, key, value):
        print("Descriptors are {}".format(self.descriptors))

        if not key in self.descriptors:
            raise KeyError()

        self.descriptors[key].validate(value)
        pass

def parse_annotation(annotation):
    """
    Convert the annotation from a type or instance, into a type
    """
    # Value is either a type, or an instance that needs turning into a type
    if isinstance(annotation, type):
        return annotation

    elif isinstance(annotation, list):
        assert type(annotation[0]) == type or type(type(annotation[0])) == type
        return ProtectedList.of(annotation[0])

    elif isinstance(annotation, tuple):
        return Enum.of(*annotation)

    else:
        raise TypeError("Unable to parse annotation value {}".format(annotation))

def model(cls):
    print("In model")
    annotations = {key: parse_annotation(annotation) for key, annotation in cls.__annotations__.items()}
    print("annotations are {}".format(annotations))
    print("Class name {}".format(cls.__name__))

    return type(cls.__name__, (cls, Model,), {'descriptors': annotations})

@model
class Sample:
    v: ("Yes", "No")
    w: (int, str)
    x: int
    y: str
    z: [int]

if __name__=='__main__':
    sample = Sample()
    sample.z.extend([1])
    sample.x = 1
    print(Sample.__bases__)
    print(Sample.descriptors)

    print(sample.__dict__)