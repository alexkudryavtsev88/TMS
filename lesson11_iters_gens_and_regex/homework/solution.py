import random


class RandomValue:

    def __init__(self, limit: int):
        self._limit = limit

    def __iter__(self):
        return RandomValueIterator(self._limit)


class RandomValueIterator:

    def __init__(self, limit: int):
        self._limit = limit
        self._pointer = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._pointer < self._limit:
            result = random.randint(1, 100)
            self._pointer += 1
            return result
        else:
            print("RandomValueIterator is stopped!")
            raise StopIteration


limit = int(input("Введите лимит: "))
my_iterable = RandomValue(limit=limit)

results = [elem for elem in my_iterable]
print(results)

assert len(results) == limit
for i in results:
    assert i is not None