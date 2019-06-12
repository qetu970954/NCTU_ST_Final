import pytest

from anytree import Node
from anytree import Walker


@pytest.fixture
def tree():
    r = Node("r")
    b = Node("b", parent=r)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=r)
    i = Node("i", parent=g)
    h = Node("h", parent=i)
    return {"r": r, "b": b, "a": a, "d": d, "c": c, "e": e, "g": g, "i": i, "h": h, }


@pytest.fixture
def walker():
    return Walker()


# The return format for a walk is:
#   (upwards, top node, downwards)
#     'upwards' is a list of node
#     'top node' is the common ancestor
#     'downwards' is a list of node
# We will test whether the return value of a walk() is identical to the expectation
def test_walking_upwards(tree, walker):
    # start from 'c', end at 'b'
    actual = walker.walk(tree["c"], tree["b"])
    expect = ((tree["c"], tree["d"],), tree["b"], ())
    assert actual == expect, "Incorrect upward path."


def test_walking_upwards2(tree, walker):
    # start from 'h', end at 'r'
    actual = walker.walk(tree["h"], tree["r"])
    expect = ((tree["h"], tree["i"], tree["g"],), tree["r"], ())
    assert actual == expect, "Incorrect upward path."


def test_walking_downwards(tree, walker):
    # start from 'b', end at 'c'
    actual = walker.walk(tree["b"], tree["c"])
    expect = ((), tree["b"], (tree["d"], tree["c"],))
    assert actual == expect, "Incorrect downward path."


def test_walking_downwards2(tree, walker):
    # start from 'r', end at 'e'
    actual = walker.walk(tree["r"], tree["e"])
    expect = ((), tree["r"], (tree["b"], tree["d"], tree["e"],))
    assert actual == expect, "Incorrect downward path."


def test_walking_from_root_to_root(tree, walker):
    # start from 'r', end at 'r'
    actual = walker.walk(tree["r"], tree["r"])
    expect = ((), tree["r"], ())
    assert actual == expect, "Incorrect walk path from root to root."


@pytest.mark.parametrize(
    ('source', 'destination', 'expectation'), [
        ("b", "g", (("b",), "r", ("g",))),
        ("a", "h", (("a", "b",), "r", ("g", "i", "h"))),
        ("i", "c", (("i", "g",), "r", ("b", "d", "c"))),
        ("b", "g", (("b",), "r", ("g",))),
    ]
)
def test_general_walking(tree, walker, source, destination, expectation):
    def enrich_expectation(a_tree, expect) -> tuple:
        # enriches the expectation by invoke tree on expectation.
        return tuple(a_tree[i] for i in expect[0]), a_tree[expect[1]], tuple(a_tree[i] for i in expect[2])

    actual = walker.walk(tree[source], tree[destination])
    assert actual == enrich_expectation(tree, expectation), "Incorrect walk path from a child to another child."


def test_walking_to_different_tree(tree, walker):
    from anytree import WalkError
    with pytest.raises(WalkError):
        walker.walk(tree["r"], Node("r"))
