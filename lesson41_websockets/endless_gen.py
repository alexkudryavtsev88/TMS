import itertools
import typing


def get_endless_gen(iter_):
    while True:
        for i_ in iter_:
            yield i_


def cycle(iter: typing.Iterable):
    result = []
    for i in iter:
        yield i
        result.append(i)

    while result:
        for elem in result:
            yield elem



endless_gen = get_endless_gen([1, 2, 3])
for i in itertools.cycle(endless_gen):
    print(i)




