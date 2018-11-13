from sample import GenericBase, GenericSample, Sample
import inspect

gb = GenericSample(n=1, x=2)
print("GB m {}".format(gb.n))

print("Serialised {}".format(gb.serialise()))

sample = Sample()
sample.c = gb
print(sample.serialise())