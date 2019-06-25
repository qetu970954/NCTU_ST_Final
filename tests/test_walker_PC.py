import pytest

from anytree import Node
from anytree import Walker


@pytest.fixture
def walker():
    return Walker()


def test_PC_1_True(walker):
    from anytree import WalkError
    with pytest.raises(WalkError):
        walker.walk(Node("r"), Node("a"))


def test_PC_1_False(walker):
    r = Node("r")
    a = Node("a", parent=r)
    b = Node("b", parent=r)
    actual = walker.walk(a, b)
    expect = ((a,), r, (b,))
    assert actual == expect


def test_PC_2_True(walker):
    r = Node("r")
    a = Node("a", parent=r)
    b = Node("b", parent=a)
    actual = walker.walk(r, b)
    expect = ((), r, (a, b,))
    assert actual == expect


def test_PC_2_False(walker):
    r = Node("r")
    a = Node("a", parent=r)
    b = Node("b", parent=a)
    c = Node("c", parent=r)
    actual = walker.walk(c, b)
    expect = ((c,), r, (a, b,))
    assert actual == expect


def test_PC_3_True(walker):
    r = Node("r")
    a = Node("a", parent=r)
    b = Node("b", parent=a)
    actual = walker.walk(b, r)
    expect = ((b, a), r, ())
    assert actual == expect


def test_PC_3_False(walker):
    r = Node("r")
    a = Node("a", parent=r)
    b = Node("b", parent=a)
    c = Node("c", parent=r)
    actual = walker.walk(b, c)
    expect = ((b, a), r, (c,))
    assert actual == expect
