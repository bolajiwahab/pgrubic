import enum

class GDPRDeletionVersion(enum.Enum):
    V1 = 1
    V2 = 2
    V3 = 3

itercars = iter(GDPRDeletionVersion)
# add 'next(itercars)' here if you also want to skip the first
next(itercars)
for car in itercars:
    print(car)
    # do work on 'prev' not 'car'
    # at end of loop:
    prev = car
# now you can do

# print(itercars)

print(GDPRDeletionVersion.V1)