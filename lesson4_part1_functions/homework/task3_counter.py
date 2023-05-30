from typing import Collection
from collections import Counter


def count_elements(collection: Collection):
    duplicates = {}

    for item in collection:
        if item not in duplicates:
            duplicates[item] = 1
        else:
            duplicates[item] += 1

    return dict(sorted(duplicates.items(), key=lambda x: x[1], reverse=True))


input_list = [1, 2, 1, 3, 4, 5, 3, 6, 7, 3, 8, 9, 4]
counter_my = count_elements(input_list)
counter_lib = Counter(input_list)

print(counter_my)
print(counter_lib)

