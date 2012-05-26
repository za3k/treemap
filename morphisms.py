from functools import partial
class Tree(object):
    def isleaf(self):
        return isinstance(self, Leaf)
    def isbranch(self):
        return isinstance(self, Branch)
class Leaf(Tree):
    def __init__(self, node):
        self.node = node
    def __str__(self):
        return str(self.node)
    def __repr__(self):
        return "Leaf({0})".format(repr(self.node))
class Branch(Tree):
    def __init__(self, n, t):
        self.branches = list(t)
        self.node = n
    def __str__(self):
        return "Branch({0},{1})".format(str(self.node),str(self.branches))
    def __repr__(self):
        return "Branch({0},{1})".format(repr(self.node),repr(self.branches))

def reducetree(leaff, branchf, tree):
    """
    The tree catamorphism.
    reduceTree (f, g) (Leaf x) = Leaf (f x)
    reduceTree (f, g) (Branch (l,r)) = g (reduceTree (f, g) l) (reduceTree (f, g) r)
    """
    if tree.isleaf(): 
        return leaff(tree.node)
    elif tree.isbranch():
        tp = partial(reducetree, leaff, branchf)
        return branchf(tree.node, list(map(tp, tree.branches)))
    else:
        assert(false)

def unspooltree1(unspool, initial):
    a,b = unspool(initial) 
    if a is not None:
        assert(b is None)
        return Leaf(a)
    elif b is not None:
        assert(a is None)
        n,t = b
        up = partial(unspooltree, unspool)
        return Branch(n, map(up, t))
    assert(False)
def unspooltree3(p, l, r, initial):
    if p(initial):
        return Leaf(l(initial))
    else:
        up = partial(unspooltree3, p, l, r)
        node, branches = r(initial)
        return Branch(node, map(up, branches))

def treemap(f, t):
    if t.isbranch():
        tt = partial(treemap, f)
        return Branch(f(t.node), map(tt, t.branches))
    elif t.isleaf():
        return Leaf(f(t.node))
    assert (false)
def treemap_with_benefits_bottomup(fl, fb, t):
    if t.isbranch():
        tt = partial(treemap_with_benefits_bottomup, fl, fb)
        newbranches = list(map(tt, t.branches))
        return Branch(fb(t.node, newbranches), newbranches)
    elif t.isleaf():
        return Leaf(fl(t.node))
    assert (false)
def treemap_with_benefits_topdown(fl, fb, t):
    if t.isbranch():
        tt = partial(treemap_with_benefits_topdown, fl, fb)
        newnode = fb(t.node, t.branches)
        return Branch(newnode, list(map(tt, t.branches)))
    elif t.isleaf():
        return Leaf(fl(t.node))
    assert (false)


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

def identity(a):
    return a

def metamorphism(l, b, p, fl, fb, i):
    return unspooltree3(p, fl, fb, reducetree(l, b, i))
def hylomorphism(p, fl, fb, l, b, i):
    return reducetree(l, b, unspooltree3(p, fl, fb))
