import pytest

import lesson4_additional.solutions as solutions
from lesson4_additional.source_dict import get_source_dict

import logging


logger = logging.getLogger("tester")
logger.setLevel(logging.DEBUG)


@pytest.fixture
def deep_dictionary():
    return get_source_dict()


@pytest.mark.parametrize(
    "source, expected", [
        (
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1]
        ),
    ]
)
def test_recursive_reverse(source, expected):
    result = solutions.recursive_reverse(source)
    assert result == expected, f"{result} != {expected}"


@pytest.mark.parametrize(
    "source, expected", [
        (
            [1, 2, 3, 4, 5],
            5
        ),
        (
            [1, 7, 0, -1, 44, 9, 28],
            44
        ),
    ]
)
def test_recursive_find_max(source, expected):
    pass



@pytest.mark.parametrize(
    "source, expected", [
        (
            [[1, 2], [3, 4], [5, 6]],
            list(range(1, 7))

        ),
        (
            [1, [2, 3], [4, 5, [6]], [7, 8], 9, 10],
            list(range(1, 11))
        ),
        (
            [[1, 2], [3, 4, [5, 6]], [7, 8, [9, 10, [11, 12]]]],
            list(range(1, 13))

        )
    ]
)
def test_recursive_flat(source, expected):
    work_func = solutions.recursive_flat
    result = work_func(source)

    assert result == expected, f"FAIL! {result} != {expected}"


@pytest.mark.parametrize(
    "lookup_value, expected", [
        ("Alex", {'val': 'Alex', 'parent': 'key3', 'deep': 1}),
        ("Mary", {'val': 'Mary', 'parent': 'key5', 'deep': 2}),
        ('Duke', {'val': 'Duke', 'parent': 'key7', 'deep': 3}),
        ('Mark', {'val': 'Mark', 'parent': 'key10', 'deep': 6})
    ]
)
def test_recursive_search_in_dict(deep_dictionary, lookup_value, expected):
    result = solutions.recursive_search(deep_dictionary, lookup_value)

    assert result == expected, f"{result} != {expected}"