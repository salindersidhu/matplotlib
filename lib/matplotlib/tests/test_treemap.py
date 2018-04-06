from matplotlib.treemap import Tree, Leaf, TreeMap
import pytest

def test_Leaf_Creation():
    l = Leaf(1)
    assert l.get_color() is None
    assert l.get_children() is None

def test_add_leaf_child():
    l = Leaf(1, "label")
    l.add_single_child("yes")
    assert l.get_children() == "yes"

def test_add_leaf_children():
    l = Leaf(1)
    l.add_multiple_children(["yes", "no"])
    assert l.get_children() == "yesno"

def test_max_leaf():
    l = Leaf(10)
    assert l.get_max_size() == 10

def test_min_leaf():
    l = Leaf(10)
    assert l.get_min_size() == 10


def test_Tree_Creation():
    l = Tree([Leaf(1),Leaf(2)])
    assert l.get_size() == 3


def test_add_tree_child():
    l = Tree([Leaf(1), Leaf(2)])
    l.add_single_child(Leaf(4))
    assert l.get_size() == 7


def test_add_tree_children():
    l = Tree([Leaf(1), Leaf(2)])
    l.add_multiple_children([Leaf(3), Leaf(4)])
    assert l.get_size() == 10


def test_max_tree():
    l = Tree([Leaf(1), Leaf(2), Tree([Leaf(9)])])
    assert l.get_max_size() == 9


def test_min_tree():
    l = Tree([Leaf(1), Leaf(2), Tree([Leaf(9)])])
    assert l.get_min_size() == 1

def test_recalculate():
    x = Leaf(1)
    l = Tree([x, Leaf(2), Tree([Leaf(9)])])
    x.set_size(10)
    l.recalculate_size()
    assert l.get_size() == 21

def test_create_tree():
    x = (Leaf(1), (Leaf(2), Leaf(3), (Leaf(4), Leaf(5)), Leaf(5)))
    tree = TreeMap.create_tree(x)
    assert tree.get_size() == 20



