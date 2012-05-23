#!/usr/bin/python
import morphisms
import os.path
from functools import partial
from operator import itemgetter, getitem
from itertools import *
from pprint import pprint

def isfile(x):
    return os.path.split(x)[1]==""
def pathsplit(x):
    h,t = os.path.split(x)
    return t,h
def splitall(path):
    return reversed(morphisms.unfold(isfile, pathsplit, path))

def issimple(x):
    _, paths, _ = x
    return len(paths)==0
def simpleprefix(x):
    prefix, _, sizes = x
    return (prefix, sizes[tuple(prefix)])
def complexprefix(x):
    prefix, paths, sizes = x
    for first, all in groupby(paths, itemgetter(0)):
        path = prefix + [first]
        shortened = [a[1:] for a in all if a[1:]]
        yield((path, shortened, sizes))
def rawtree():
    sizes = {}
    with open("rawdata") as f:
        for line in f:
            size, file = line.rstrip().split(None, 1)
            sizes[tuple(splitall(file))] = int(size)
    paths = list(sorted(sizes.keys()))
    return morphisms.unspooltree3(
        issimple,
        simpleprefix,
        complexprefix,
        ([], paths, sizes), )

def alternating_layout(tree):
    return tree

def annotate_leaf(l):
    p,s = l
    return False, None, p, s
def annotate_branch(a):
    assert(len(a)>0) #There's a child
    assert(len(a[0][2])>0) #And it has a path
    path = a[0][2][:-1]
    for child in a:
        assert(child[2][:-1]==path) #and all the children have the same parent
    return True, a, path, sum(map(itemgetter(3), a))
def annotate_tree(tree):
    return morphisms.reducetree(annotate_leaf, annotate_branch, tree)



if __name__=='__main__':
    input = rawtree()
    annotated = annotate_tree(input)
    simple_layout = alternating_layout(annotated)
    pprint(simple_layout)
