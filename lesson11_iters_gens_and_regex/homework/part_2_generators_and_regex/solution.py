""" Task 1 """

import re

p = r"\+[0-9]{1,3}-[0-9]{2}-[0-9]{5,7}"
comp = re.compile(p)

valid = (
    "+375-29-7776655",
    "+37-29-7776655",
    "+3-29-7776655",
    "+375-44-777665",
    "+375-44-77766",
)

invalid = (
    "",

    "375-29-7776655",

    "+-29-7776655",
    "+3a5-29-7776655",
    "+3756-29-7776655",

    "+375--7776655",
    "+375-4-7776655",
    "+375-444-7776655",
    "+375-c4-7776655",

    "+375-33-",
    "+375-33-7",
    "+375-33-7776",
    "+375-33-77766554",
    "+375-29-7776e55",
)

for n in valid:
    res = comp.fullmatch(n)
    assert res.group() == n

for n2 in invalid:
    assert comp.fullmatch(n2) is None