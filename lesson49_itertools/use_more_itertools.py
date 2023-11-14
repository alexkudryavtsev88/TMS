import more_itertools as mit

ITERABLE = (1, 2, 3, 4, 5, 6, 7)
N = 3
SEP = "-" * 10
MESSAGE = "'{}':\n IN: {}, N = {};\n OUT: {}\n{}"

"""
--------------------------------------
    GROUPING
--------------------------------------
"""

"""
CHUNKED:

Break input ITERABLE into the LISTS with length N:
If ITERABLE length is not divided by N:
- the last LIST has length < N (can have length 1)
- if optional kwarg 'strict' == True, error is raised

Returns: Iterator with Lists
"""

chunked_res = mit.chunked(ITERABLE, N)
act = list(chunked_res)
print(MESSAGE.format("chunked", ITERABLE, N, act, SEP))
assert act == [[1, 2, 3], [4, 5, 6], [7]]

# --------------------------------------

"""
ICHUNKED:

The same as 'chunked'

Returns: Iterator with islice objects
"""
ichunked_res = mit.ichunked(ITERABLE, N)
act = [list(i) for i in ichunked_res]
print(MESSAGE.format("ichunked", ITERABLE, N, act, SEP))
assert act == [[1, 2, 3], [4, 5, 6], [7]]

# --------------------------------------

"""
CHUNKED_EVEN:

The same as 'chunked', but
- input ITERABLE is broken to LISTS of approximately length N.
- Items are distributed such the lengths of the lists differ by at most 1 item

Returns: Iterator with Lists
"""
chunked_even_res = mit.chunked_even(ITERABLE, N)
act = list(chunked_even_res)
print(MESSAGE.format("chunked_even", ITERABLE, N, act, SEP))
assert act == [[1, 2, 3], [4, 5], [6, 7]]

# --------------------------------------

"""
SLICED

The same as 'chunked', but:
- cannot use with ITERABLES which don't support Slicing
- output ITERATOR contains the Objects with same type as input ITERABLE

Returns: Iterator with Objects of input Iterable type
"""
sliced_res = mit.sliced(ITERABLE, N)
act = list(sliced_res)
print(MESSAGE.format("sliced", ITERABLE, N, act, SEP))
assert act == [(1, 2, 3), (4, 5, 6), (7,)]

# --------------------------------------

"""
DISTRIBUTE

Distribute the items from ITERABLE among N smaller iterables
- Elements from input ITERABLE will be grouped though N positions
- Count of ITERATORS (each group) will be <= N

Returns: List of Iterators
"""
n, iterable = 2, [1, 2, 3, 4, 5, 6]
distrib_res = mit.distribute(n, iterable)
act = [list(c) for c in distrib_res]
print(MESSAGE.format("distribute", iterable, n, act, SEP))
assert act == [[1, 3, 5], [2, 4, 6]]

"""If the length of ITERABLE is not evenly divisible by N, then the
length of the returned ITERABLES will not be identical"""
n, iterable = 2, [1, 2, 3, 4, 5, 6, 7]
distrib_res2 = mit.distribute(n, iterable)
act2 = [list(c) for c in distrib_res2]
print(MESSAGE.format("distribute", iterable, n, act2, SEP))
assert act2 == [[1, 3, 5, 7], [2, 4, 6]]

"""If the length of ITERABLE is smaller than N, then the last returned
iterables will be empty"""
n, iterable = 5, [1, 2, 3]
distrib_res3 = mit.distribute(n, iterable)
act3 = [list(c) for c in distrib_res3]
print(MESSAGE.format("distribute", iterable, n, act3, SEP))
assert act3 == [[1], [2], [3], [], []]

# --------------------------------------

"""DIVIDE

- Divide the elements from iterable into N parts, maintaining order
- If the length of iterable is not evenly divisible by n,
then the length of the returned iterables will not be identical

Returns: List of Iterators
"""
n = 4
iterable = (1, 2, 3, 4, 5, 6)
divide_res = mit.divide(n, iterable)
act = [list(i) for i in divide_res]
print(MESSAGE.format("divide", iterable, n, act, SEP))
assert act == [[1, 2], [3, 4], [5], [6]]

"""If the length of ITERABLE is not evenly divisible by N, then the
length of the returned ITERABLES will not be identical"""
divide_res2 = mit.divide(n, ITERABLE)
act2 = [list(i) for i in divide_res2]
print(MESSAGE.format("divide", ITERABLE, n, act2, SEP))
assert act2 == [[1, 2], [3, 4], [5, 6], [7]]

"""If the length of ITERABLE is smaller than N, then the last returned
iterables will be empty"""
n, iterable = 5, [1, 2, 3]
divide_res3 = mit.divide(n, iterable)
act3 = [list(c) for c in divide_res3]
print(MESSAGE.format("divide", iterable, n, act3, SEP))
assert act3 == [[1], [2], [3], [], []]

# --------------------------------------

"""SPLIT_AT

Break Iterable into Lists by Separator: Element for which the bool func returns True

Returns: Iterator with Lists"""
fnc = lambda x: x.isupper()

"""Separator element is not included if 'keep_separator' is False (by default)"""
split_at_res = mit.split_at("_OneTwo", fnc)
act = list(split_at_res)
print(act)
assert act == [["_"], ["n", "e"], ["w", "o"]]
"""and included if 'keep_separator' is True"""
split_at_res = mit.split_at("_OneTwo", fnc, keep_separator=True)
act = list(split_at_res)
print(act)
assert act == [["_"], ["O"], ["n", "e"], ["T"], ["w", "o"]]
"""if Separator element stays first/last in the input Iterable:
   empty List will be added as first/last element of the output Iterator"""
split_at_res = mit.split_at("OneTwoZ", fnc, keep_separator=True)
act = list(split_at_res)
print(act)
assert act == [[], ["O"], ["n", "e"], ["T"], ["w", "o"], ["Z"], []]

"""max_split defines count of splitting"""
split_at_res = mit.split_at("OneTwoZaaa", fnc, maxsplit=2, keep_separator=True)
act = list(split_at_res)
print(act)
assert act == [
    [],
    ["O"],
    ["n", "e"],
    ["T"],
    ["w", "o", "Z", "a", "a", "a"],  # last capital char is not dropped
]

"""SPLIT_BEFORE

Break Iterable into Lists where each List ends just before an item for which bool func returns True"""
split_before_res = mit.split_before("123OneTwoZoo", fnc)
act = list(split_before_res)
print(act)
assert act == [["1", "2", "3"], ["O", "n", "e"], ["T", "w", "o"], ["Z", "o", "o"]]

"""SPLIT_AFTER

Break Iterable into Lists where each List ends with an item where callable pred return"""
split_after_res = mit.split_after("123OneTwoZoo", fnc)
act = list(split_after_res)
print(act)
assert act == [["1", "2", "3", "O"], ["n", "e", "T"], ["w", "o", "Z"], ["o", "o"]]

"""SPLIT_INTO

Break Iterable into Lists where each List has length == appropriate int in 'sizes"""
split_into_res = mit.split_into((1, 2, 3, 4, 5, 6, 7, 8), [1, 2, 3])
act = list(split_into_res)
print(act)
assert act == [[1], [2, 3], [4, 5, 6]]  # items after 6 are dropped

"""SPLIT_WHEN"""
