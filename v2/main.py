from sample import GenericBase, GenericSample, Sample
import inspect
import timeit

gb = GenericSample(n=1, x=2)
print("GB m {}".format(gb.n))

print("Serialised {}".format(gb.serialise()))

sample = Sample()
sample.c = gb
sample.d = [1]
serialised = sample.serialise()
new = Sample.deserialise(serialised)

print(sample.__dict__)
print(new.__dict__)
print(new.serialise())
