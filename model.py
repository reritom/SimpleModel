

class Model(type):
    def __new__(cls, name, bases, dct):
        # Get all the descriptors for this class from the annotations and parent annotations
        descriptors = {key: value for base in bases for key, value in base.__dict__.get('__annotations__').items()}
        descriptors.update(dct.get('__annotations__'))
        dct.update({'descriptors': descriptors})

        class Meta(cls):
            def serialise(self):
                print("serialise")
                pass

            def deserialise(self, serialised):
                pass

        print(cls)
        # Create a new class
        x = super().__new__(cls, name, (Meta, *bases,), dct)
        return x
