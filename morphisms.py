from functools import partial
class Tree(object):
    def isleaf(self):
        return isinstance(self, Leaf)
    def isbranch(self):
        return isinstance(self, Branch)
class Leaf(Tree):
    def __init__(self, ob):
        self.ob = ob
    def __str__(self):
        return str(self.ob)
    def __repr__(self):
        return "Leaf({0})".format(repr(self.ob))
class Branch(Tree):
    def __init__(self, t):
        self.branches = list(t)
    def __str__(self):
        return str(self.branches)
    def __repr__(self):
        return "Branch({0})".format(repr(self.branches))

def reducetree(leaff, branchf, tree):
    """
    The tree catamorphism.
    reduceTree (f, g) (Leaf x) = Leaf (f x)
    reduceTree (f, g) (Branch (l,r)) = g (reduceTree (f, g) l) (reduceTree (f, g) r)
    """
    if tree.isleaf(): 
        return leaff(tree.ob)
    elif tree.isbranch():
        tp = partial(reducetree, leaff, branchf)
        return branchf(list(map(tp, tree.branches)))
    else:
        assert(false)

def unspooltree1(unspool, initial):
    a,b = unspool(initial) 
    if a is not None:
        assert(b is None)
        return Leaf(a)
    elif b is not None:
        assert(a is None)
        up = partial(unspooltree, unspool)
        return Branch(map(up, b))
    assert(False)
def unspooltree3(p, l, r, initial):
    if p(initial):
        return Leaf(l(initial))
    else:
        up = partial(unspooltree3, p, l, r)
        return Branch(map(up, r(initial)))

def treemap(f, t):
    if t.isbranch():
        tt = partial(treemap, f)
        return Branch(map(tt, t.branches))
    elif t.isleaf():
        return Leaf(f(t.ob))
    assert(false)

def unfold(p, f, initial):
    """
    Anamorphism on lists
    """
    if p(initial):
        return []
    else:
        a, b = f(initial)
        up = partial(unfold, p, f)
        return [a] + up(b)

def metamorphism(l, b, p, fl, fb, i):
    return unspooltree3(p, fl, fb, reducetree(l, b, i))
def hylomorphism(p, fl, fb, l, b, i):
    return reducetree(l, b, unspooltree3(p, fl, fb))
