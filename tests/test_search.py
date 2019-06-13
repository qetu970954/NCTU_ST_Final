import pytest

from anytree import Node
from anytree import find, find_by_attr
from anytree import findall, findall_by_attr
from anytree import CountError


'''
@pytest.fixture
def tree_findall():
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    return {"f": f, "b": b, "a": a, "d": d, "c": c, "e": e, }


testdata_findall[
    ("f", lambda node: node.name in ("a", "b"), ("b","a"), None),
    ("f", lambda node: d in node.path, ("b","a"), None),
]
@pytest.mark.parametrize("root, lambda_, expected, exception", testdata_findall)
def test_findall(tree_findall, root , lambda_, exception):
    if exception is None:
        assert findall(tree_findall[root], filter_=lambda_) ==  
    elif exception is CountError:
    
def test_findall1(tree_findall):
    assert findall(tree_findall["f"], filter_=lambda node: node.name in ("a", "b")) == (tree_findall["b"], tree_findall["a"])
    assert findall(tree_findall["f"], filter_=lambda node: tree_findall["d"] in node.path) == (tree_findall["d"], tree_findall["c"], tree_findall["e"])
'''


def test_findall_normal():
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    assert findall(f, filter_=lambda node: node.name in ("a", "b")) == (b, a)
    assert findall(f, filter_=lambda node: d in node.path) == (d, c, e)
    assert findall(f, filter_=lambda node: d in node.path, stop=lambda node: node.parent is d) == (d,)
    assert findall(f, filter_=lambda node: d in node.path, maxlevel=3) == (d,)


def test_findall_counterror_mincount():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)
    with pytest.raises(CountError):
        findall(f, filter_=lambda node: d in node.path, mincount=4)
    with pytest.raises(CountError):
        findall(f, filter_=lambda node: node.name in ("x", "y", "z"), mincount=1)


def test_findall_counterror_maxcount():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)
    with pytest.raises(CountError):
        findall(f, filter_=lambda node: d in node.path, maxcount=2)
    with pytest.raises(CountError):
        findall(f, filter_=lambda node: f in node.path, maxcount=5)


def test_findall_by_attr_normal():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)

    assert findall_by_attr(f, "d") == (d,)
    assert findall_by_attr(f, d, name="parent") == (c, e)
    assert findall_by_attr(f, d, name="parent", maxlevel=2) == ()


def test_findall_by_attr_counterror_mincount():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)

    with pytest.raises(CountError):
        findall_by_attr(f, "z", mincount=1)
    with pytest.raises(CountError):
        findall_by_attr(f, b, name="parent", mincount=3)


def test_findall_by_attr_counterror_maxcount():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)

    with pytest.raises(CountError):
        findall_by_attr(f, d, name="parent", maxcount=1)


def test_find_normal():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    Node("h", parent=i)

    assert find(f, lambda n: n.name == "d") == d
    assert find(f, lambda n: n.name == "z") is None


def test_find_counterror():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    Node("h", parent=i)

    with pytest.raises(CountError):
        find(f, lambda n: b in n.path)
    with pytest.raises(CountError):
        find(f, lambda n: n.parent == f)


'''
@pytest.fixture
def tree_find_by_attr():
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d, foo=4)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)
    return {"f": f, "b": b, "a": a, "d": d, "c": c, "e": e, "g": g, "i": i, "h": h,}

testdata_find_by_attr[
    ("f", "d", "name", "d", None),
    ("f", 4, "foo", "c", None),
    ("f", 8, "foo", None, None),
]

@pytest.mark.parametrize("root, value_ , name_, expected, exception", testdata_find_by_attr())
def test_find_by_attr():
    if exception == None:
        assert find_by_attr(tree_find_by_attr[root], "d") == expected
    elif exception == CountError:
'''


def test_find_by_attr():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d, foo=4)
    Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    Node("h", parent=i)

    assert find_by_attr(f, "d") == d
    assert find_by_attr(f, name="foo", value=4) == c
    assert find_by_attr(f, name="foo", value=8) is None


def test_find_by_attr_counterror():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d, foo=4)
    Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    Node("h", parent=i)

    with pytest.raises(CountError):
        find_by_attr(f, name="parent", value=f)

