class MyList:
    def __init__(self, list_):
        self._list = list_

    def __str__(self):
        return f"MyList object: {self._list}"

    def __iter__(self):
        for item in self._list:
            yield item

    def __len__(self):
        return len(self._list)

    def __contains__(self, item):
        return item in self._list

    def __add__(self, other):
        return self._list + other._list

    def __getitem__(self, item: int):
        return self._list[item]

    def __setitem__(self, key: int, value):
        self._list[key] = value

    def __call__(self, *args, **kwargs):
        print(self.__str__())


my_list = MyList([1, 2, 3, 4, 5])
my_list()  # вызов __call__

for message in my_list:  # в цикле вызывается __iter__
    print(message)

print(f"Length: {len(my_list)}")  # вызов __len__

print(6 in my_list)  # вызов __contains__

lists_sum = my_list + MyList([10, 11, 12])  # вызов __add__
print(lists_sum)

print(my_list[0])  # вызов __getitem__
my_list[1] = 100   # вызов __setitem__

print(my_list)     # вызов __str__

