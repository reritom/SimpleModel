from sample import GenericBase, GenericSample, Sample
import inspect

gb = GenericSample(n=1, x=2)
print("GB m {}".format(gb.n))

print("Serialised {}".format(gb.serialise()))

sample = Sample()
sample.c = gb
serialised = sample.serialise()
new = Sample.deserialise(serialised)

print(sample.__dict__)
print(new.__dict__)