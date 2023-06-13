from typing import Collection


class StringList:
    def __init__(self, source: Collection):
        self._list = [str(i) for i in source]

    def __str__(self):
        return f"MyList{self._list} object at <{id(self)}>"

    def __iter__(self):
        """Iterate over the inner list"""
        for item in self._list:
            yield item

    def __len__(self):
        return len(self._list)

    def __contains__(self, item):
        """Returns True if the specified item is in inner list"""
        return item in self._list

    def __add__(self, other):
        """
        Returns the new Instance of StringClass
        with inner list which is concatenated from the previous list
        and the inner list of 'other' object
        """
        return self.__class__(source=self._list + other._list)

    def __getitem__(self, item: int) -> str:
        """Get element by the specified index from the inner list"""
        return self._list[item]

    def __setitem__(self, idx: int, value):
        """Set element by the specified index to the inner list"""
        try:
            self._list[idx] = str(value)
        except IndexError:
            raise IndexError(f"Index {idx} doesn't exist in {self}")

    def __call__(self, *args, **kwargs):
        print(f"{self} is called!")

    def append(self, item: int):
        self._list.append(str(item))

    def pop(self, index: int | None = None) -> str:
        if index is None:
            index = len(self._list) - 1

        return self._list.pop(index)


my_list = StringList([1, 2, 3, 4, 5])
my_list()  # вызов __call__

for message in my_list:  # в цикле вызывается __iter__
    print(message)

print(f"Length: {len(my_list)}")  # вызов __len__

print(6 in my_list)  # вызов __contains__

lists_sum = my_list + StringList([10, 11, 12])  # вызов __add__
print(lists_sum)

print(my_list[0])  # вызов __getitem__
my_list[1] = 100   # вызов __setitem__

print(my_list)     # вызов __str__

