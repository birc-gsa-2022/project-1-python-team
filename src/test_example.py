# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_
from lin import lin
from naive import naive


def test_1984():
    assert 2 + 2 == 4


x = "mississippi"
p = "iss"


print(naive(x, p))
print(lin(x, p))
