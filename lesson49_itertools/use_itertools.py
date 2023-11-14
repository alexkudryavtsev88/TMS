import itertools as it
import operator

"""
--------------------------------------
    INFINITE ITERATORS
--------------------------------------
"""

# it.repeat('10', 5) / it.repeat('10') -- Repeat '10' 5 times / endlessly
# it.cycle(iterable)                   -- Generator obj, will be repeated after exhausting (endlessly)
# it.count(10) / it.count()            -- Generate endless sequence of integers started from 10 / 0

"""
--------------------------------------
   TERMINAL ITERATORS
--------------------------------------
"""

""" ACCUMULATE:

returns iterator which contains accumulated result of sum for each iteration """
accumulate_res = it.accumulate((1, 2, 3))
assert list(accumulate_res) == [1, 3, 6]

""" CHAIN

chain.from_iterable: Join iterables objects from common iterable object got from single arg"""
chain_iter_res = it.chain.from_iterable([[1, 2, 3], [4, 5, 6]])
assert list(chain_iter_res) == [1, 2, 3, 4, 5, 6]

"""chain: Join iterables objects got from positional args"""
chain_res = it.chain([1, 2, 3], [4, 5, 6])
assert list(chain_res) == [1, 2, 3, 4, 5, 6]

"""chain: another variant of using: Join generator objects got from positional args"""
chain_res_gen = it.chain(
    (i for i in range(1, 4)), (j for j in range(4, 8)), (k for k in range(8, 13))
)
assert list(chain_res_gen) == list(range(1, 13))

# --------------------------------------

""" COMPRESS

returns Iterator with 1st Iterable's elements
which positions correspond to positions of TRUE in 2nd Iterable"""
criteria = (False, True, True, False)
compress_res = it.compress([1, 2, 3, 4], criteria)
assert list(compress_res) == [2, 3]

"""Another variants of usage
NOTE: first arg may be String, but second arg should have iterable type except String"""
compress_res2 = it.compress("1234", (0, 1, 1, 0))
assert list(compress_res2) == ["2", "3"]

# --------------------------------------

"""DROPWHILE

- drop elements from Iterable (second arg) until the bool func (first arg) returns TRUE
- save all elements from that moment when the bool func has returned FALSE

Boolean func, checks is 'x' an Odd number or not"""
is_odd = lambda x: x % 2 == 0
iterable = [0, 2, 4, 6, 8, 3, 10, 5]
"""Example 1: first five elements of Iterable are Odd numbers.
These five elements will be dropped.
ALL NEXT elements will be saved regardless of whether they are Odd numbers or not"""
dropwhile_res = it.dropwhile(is_odd, iterable)
act = list(dropwhile_res)
assert act == [
    3,
    10,
    5,
]  # 10 is Odd number but it's SAVED because stays after the Even number 3

"""Example 2: first element of Iterable is EVEN number.
NO ONE element will be dropped."""
dropwhile_res2 = it.dropwhile(is_odd, [1] + iterable)
act = list(dropwhile_res2)
assert act == [1, 0, 2, 4, 6, 8, 3, 10, 5]

# --------------------------------------

"""TAKEWHILE

- save elements from Iterable (second arg) until the bool func (first arg) returns TRUE
- drop all elements from that moment when the bool func has returned FALSE

 Boolean func, checks is 'x' an Odd number or not"""
is_odd = lambda x: x % 2 == 0
iterable = [0, 2, 4, 6, 8, 3, 10, 5]
"""Example 1: first five elements of Iterable are Odd numbers.
These five elements will be saved.
ALL NEXT elements will be dropped regardless of whether they are Odd numbers or not"""
takewhile_res = it.takewhile(is_odd, iterable)
act = list(takewhile_res)
assert act == [
    0,
    2,
    4,
    6,
    8,
]  # 4 is Odd number but it's DROPPED because stays after the Even number 3

"""Example 2: first element of Iterable is EVEN number.
ALL elements will be dropped"""
takewhile_res2 = it.takewhile(is_odd, [1] + iterable)
act = list(takewhile_res2)
assert act == []

# --------------------------------------

"""FILTERFALSE

skip all elements from iterable (second arg) for which the bool func (first arg) has returned True"""
is_odd = lambda x: x % 2 == 0
filterfalse_res = it.filterfalse(is_odd, [0, 1, 2, 3, 4, 5])
act = list(filterfalse_res)
assert act == [1, 3, 5]

# --------------------------------------

"""GROUPBY

make groups with n neighbours for which the key func returns the same bool result
Example 1: key func checks that String Item starts with "A" letter

Expected result:
- 'Alex' and 'Ann' will be grouped together because they are neighbours and for both key func returns TRUE
- 'Belarus' will be grouped alone because key func for it returns FALSE
   but for its LEFT neighbour ('Ann') the key func returned TRUE
- 'America' will be grouped alone because key func for it returns TRUE
   but for its LEFT neighbour ('Belarus') the key func returned FALSE
- 'Olga' and 'Irina' will be grouped together, because they are neighbours, for both items the key func returns FALSE,
   and for LEFT neighbour of the first item ('Olga') the key func returned TRUE"""

group_func = lambda item: item.startswith("A")
groupby_res = it.groupby(
    ["Alex", "Ann", "Belarus", "America", "Olga", "Irina"], key=group_func
)
groupby_res = [list(g) for k, g in groupby_res]
assert groupby_res == [["Alex", "Ann"], ["Belarus"], ["America"], ["Olga", "Irina"]]

"""Example 2: key func is not specified, then func 'lambda x: x' will be used
Neighbour elements will be grouped by equality each other"""
groupby_res2 = [list(g) for k, g in it.groupby("AAAABBBCCD")]
assert groupby_res2 == [["A", "A", "A", "A"], ["B", "B", "B"], ["C", "C"], ["D"]]

# --------------------------------------

"""ZIP_LONGEST

works as built-in 'zip' func, but builds final Iterator until the Longest Iterable ends
if 1st and 2nd Iterables has different length:
'fillvalue' or None will be set as pair for 'alone' elements

Example 1:
- 1st Iterable (Keys) is Longer than 2nd Iterable (Values): final dict will have length of 1st Iterable
- 'D', 'E', 'F' Keys don't have appropriate Values in 2nd Iterable:
  they will be paired with None (because 'fillvalue' is not specified)"""
ziplong_res = it.zip_longest("ABCDEF", (1, 2, 3))
assert dict(ziplong_res) == {"A": 1, "B": 2, "C": 3, "D": None, "E": None, "F": None}

"""Example 2:
- Same, but 'D', 'E', 'F' Keys will be paired with int 0 value"""
ziplong_res2 = it.zip_longest("ABCDEF", (1, 2, 3), fillvalue=0)
assert dict(ziplong_res2) == {"A": 1, "B": 2, "C": 3, "D": 0, "E": 0, "F": 0}

"""Example 3:
- 1st Iterable (keys) is Shorter than 2nd Iterable (values):
int 0 value will be set as Key for 'D', 'E', 'F' Values, but Keys should be unique,
therefore only FIRST pair with 0 Key (0, 'F') will be in Final Dict"""
ziplong_res3 = it.zip_longest((1, 2, 3), "ABCDEF", fillvalue=0)
assert dict(ziplong_res3) == {1: "A", 2: "B", 3: "C", 0: "F"}

# --------------------------------------

"""STARMAP

- Got func as 1st argument, Iterable of Iterables as 2nd argument
- Apply func to each Iterable in 2nd arg Iterable

Example 1: apply multiplication to each tuple in 'iter_obj':
1st tuple element will be multiplied with the 2nd tuple element"""
iter_obj = [(1, 2), (4, 5), (7, 8)]
starmap_res = it.starmap(operator.mul, iter_obj)
assert list(starmap_res) == [2, 20, 56]

"""Example 2: key func makes sum of 5 elements
each tuple in 'iter_obj2' should contains 5 elements strictly"""
key_func = lambda x, y, z, i, j: x + y + z + i + j
iter1, iter2, iter3 = (1, 2, 3, 4, 5), (6, 7, 8, 9, 10), (10, 20, 30, 40, 50)
iter_obj2 = [iter1, iter2, iter3]

starmap_res2 = it.starmap(key_func, iter_obj2)
assert list(starmap_res2) == [sum(iter1), sum(iter2), sum(iter3)]

# --------------------------------------

"""ISLICE:
- make the same as built-in 'slice' but returns Iterator
- doesn't work with negative indices !
- 1st arg - required, Iterable
- 2nd arg - required, int
- 3rd and 4th args - optional, int"""

iter_obj = (1, 2, 3, 4, 5)

"""EXAMPLE 1:
- if only 2 positional args are specified:
  2nd arg is defined as 'stop', 'start' is 0 (by default), 'step' is 1 (by default)
  result Iterator will contain Iterable's elements from 0 to 3 indices"""
islice_res1 = it.islice(iter_obj, 4)
assert list(islice_res1) == [1, 2, 3, 4]

"""EXAMPLE 2:
- if only 3 positional args are specified:
  2nd arg is defined as 'start', 3rd arg is 'stop', 'step' is 1 (by default)
  result Iterator will contain Iterable's elements from 1 to 3 indices"""
islice_res2 = it.islice(iter_obj, 1, 4)
assert list(islice_res2) == [2, 3, 4]

"""EXAMPLE 3:
- if all 4 args are specified:
  2nd arg is 'start', 3rd arg is 'stop', 4th arg is 'step'
  result Iterator will contain Iterable's elements from 0 to 3 indices with step 2"""
islice_res3 = it.islice(iter_obj, 0, 4, 2)
assert list(islice_res3) == [1, 3]

# --------------------------------------

"""TEE:
returns tuple with N independent Iterators from Input Iterable"""
n_count = 5
iter_obj = [1, 2, 3, 4, 5]
tee_res = it.tee(iter_obj, n_count)

for i in range(n_count):
    assert list(tee_res[i]) == iter_obj

"""
--------------------------------------
   COMBINATORIAL ITERATORS
---------------------------------------
"""

"""PRODUCT:

Cartesian product of elements from iterables got as args"""

"""Example 1"""
product_res = it.product(("A",), (1, 2, 3))

assert list(product_res) == [
    ("A", 1),
    ("A", 2),
    ("A", 3),
]

"""Example 2: with 'repeat' arg = 2"""
product_res = it.product(("A",), (1, 2, 3), repeat=2)
assert list(product_res) == [
    ("A", 1, "A", 1),
    ("A", 1, "A", 2),
    ("A", 1, "A", 3),
    ("A", 2, "A", 1),
    ("A", 2, "A", 2),
    ("A", 2, "A", 3),
    ("A", 3, "A", 1),
    ("A", 3, "A", 2),
    ("A", 3, "A", 3),
]

# --------------------------------------

"""PERMUTATIONS

- Returns all permutations of elements in input Iterable
- second optional argument is count of permutations (default count is length of Iterable)
- tuples in result Iterator is ordered lexicographically
- can contain not unique tuples"""

"""Example 1: perm count is not specified and will be set as 3 by default"""
perm_res = it.permutations([1, 2, 3])
assert list(perm_res) == [
    (1, 2, 3),
    (1, 3, 2),
    (2, 1, 3),
    (2, 3, 1),
    (3, 1, 2),
    (3, 2, 1),
]

"""Example 2: perm count is specified as 2"""
perm_res = it.permutations([1, 2, 3], 2)
assert list(perm_res) == [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

"""Example 3:
elements in result Iterator are unique but by position, not by value"""
perm_res = it.permutations([1, 1])
assert list(perm_res) == [(1, 1), (1, 1)]
# 2 combinations: 1st -> 2nd; 2nd -> 1st: regardless of the 1st and 2nd equality

"""COMBINATIONS

- Returns combinations of elements
- Length of each combination (tuple) equal to N (second arg)
- Can NOT contain not unique tuples"""
comb_res = it.combinations([1, 2, 3], 2)
assert list(comb_res) == [(1, 2), (1, 3), (2, 3)]
# (2, 1), (3, 1), (3, 2) - combinations are NOT unique, than skipped.

"""Example 2"""
comb_res2 = it.combinations([1, 1], 2)
assert list(comb_res2) == [(1, 1)]
# only 1 unique combination

"""COMBINATIONS_WITH_REPLACEMENT

Same as 'combinations' but include combinations of elements with itself"""
comb_res_repl = it.combinations_with_replacement([1, 2, 3], 2)
assert list(comb_res_repl) == [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
# (1, 1), (2, 2), (3, 3) - combinations of elements 1, 2, 3 with ITSELF
# (2, 1), (3, 1), (3, 2) - combinations are NOT unique, than skipped.

comb_res_repl2 = it.combinations_with_replacement([1, 1], 2)
assert list(comb_res_repl2) == [
    (1, 1),
    (1, 1),
    (1, 1),
]
# 3 combinations: 1st -> ITSELF, 1st -> 2nd, 2nd -> ITSELF: regardless of 1st and 2nd equality
