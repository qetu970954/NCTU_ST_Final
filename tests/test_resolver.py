# -*- coding: utf-8 -*-
import pytest

from anytree import Node
from anytree import Resolver, ChildResolverError, ResolverError

@pytest.fixture
def tree_get():
    top = Node("top", parent=None)
    sub0 = Node("sub0", parent=top)
    sub0sub0 = Node("sub0sub0", parent=sub0)
    sub0sub1 = Node("sub0sub1", parent=sub0)
    sub1 = Node("sub1", parent=top)
    ath = Node("ath", parent=None)
    athsub = Node("athsub", parent=ath)
    return {"top": top, "sub0": sub0, "sub0sub0": sub0sub0, "sub0sub1": sub0sub1, "sub1": sub1, "ath": ath, "athsub": athsub,}

testdata_get = [
    # Relative paths
    ("top", "sub0/sub0sub0", "sub0sub0", None),
    ("sub1", "..", "top", None),
    ("sub1", "../sub0/sub0sub1", "sub0sub1", None),
    ("sub1", ".", "sub1", None),
    ("sub1", "", "sub1", None),
    # Absolute paths
    ("sub0sub0","/top", "top", None),
    ("sub0sub0", "/top/sub0", "sub0",None),
    # Exception for three cases
    ("top", "sub2", "", ChildResolverError),        # same tree
    ("athsub", "../sub0", "", ChildResolverError),    # other tree
    ("sub0sub0", "/", "", ResolverError),           # root missing
    ("sub0sub0", "/sbar", "", ResolverError),        # unknow root node
]

@pytest.fixture
def resolver():
    return Resolver('name')

@pytest.mark.parametrize("source, path, expected, exception", testdata_get)
def test_get(tree_get, resolver, source, path, expected, exception):
    if exception is None:
        actual = resolver.get(tree_get[source], path)
        expected = tree_get[expected]
        assert actual == expected
    elif exception is ChildResolverError:
        with pytest.raises(exception, message="%s has no child %s. Children are: 'sub0', 'sub1'."%(tree_get[source], path)):
            resolver.get(tree_get[source], path)
    elif exception is ResolverError:
        with pytest.raises(exception):
            resolver.get(tree_get[source], path)

@pytest.fixture
def tree_glob():
    top = Node("top", parent=None)
    sub0 = Node("sub0", parent=top)
    sub0sub0 = Node("sub0", parent=sub0)
    sub0sub1 = Node("sub1", parent=sub0)
    sub1 = Node("sub1", parent=top)
    sub1sub0 = Node("sub0", parent=sub1)
    nothing = []
    return {"top": top, "sub0": sub0, "sub0sub0": sub0sub0, "sub0sub1": sub0sub1, "sub1": sub1, "sub1sub0": sub1sub0, " ": nothing}

testdata_glob = [
    # Relative paths
    ("top", "sub0/sub?", "sub0sub0, sub0sub1", None),       # test "?"
    ("sub1", ".././*", "sub0, sub1", None),                 # test "*"
    ("top", "*/*", "sub0sub0, sub0sub1, sub1sub0", None),
    ("top", "*/sub0", "sub0sub0, sub1sub0", None),
    ("top", "sub1/sub1", "", ChildResolverError),
    # Non-matching wildcards are no error
    ("top", "sbar*", " ", None),
    ("top", "sub2", "", ChildResolverError),
    # Absolute paths
    ("sub0sub0", "/top/*", "sub0, sub1", None),
    ("sub0sub0", "/", "", ResolverError),           # root missing
    ("sub0sub0", "/sbar", "", ResolverError),        # unknow root node
]

@pytest.mark.parametrize("source, path, expected, exception", testdata_glob)
def test_glob(tree_glob, resolver, source, path, expected, exception):
    #  support Wildcard : '?', '*'
    if exception is None:
        actual = resolver.glob(tree_glob[source], path)
        if expected != " ":
            expected = expected.split(", ")
            count = 0
            for ans in expected:
                assert actual[count] == tree_glob[ans]
                count += 1
        # test for non-matching []
        else :
            assert actual == tree_glob[expected]
    elif exception is ChildResolverError:
        with pytest.raises(exception):
            resolver.glob(tree_glob[source], path)
    elif exception is ResolverError:
        with pytest.raises(exception):
            resolver.glob(tree_glob[source], path)



def test_glob_cache():
    """Wildcard Cache."""
    #  make tree
    top = Node("top")
    for i in range(21):
        name = "sub" + str(i)
        i = Node(name, parent=top)
    r = Resolver()
    Resolver._match_cache.clear()

    # test case
    for i in range(21):
        name = "sub" + str(i)
        #assert len(Resolver._match_cache) == i
        r.glob(top, name)
    # up to max cache size 20
    # test if it will do Resolver._match_cache.clear()
    assert len(Resolver._match_cache) == 1