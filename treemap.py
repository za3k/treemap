#!/usr/bin/python
import morphisms
import os.path
from functools import partial
from operator import itemgetter, getitem
from itertools import *
from pprint import pprint
import json

def isfile(x):
    return os.path.split(x)[1]==""
def pathsplit(x):
    h,t = os.path.split(x)
    return t,h
def splitall(path):
    return reversed(morphisms.unfold(isfile, pathsplit, path))

def identity(*a):
    return a

def issimple(x):
    _, paths, _ = x
    return len(paths)==0
def simpleprefix(x):
    prefix, _, sizes = x
    return (prefix, sizes[tuple(prefix)])
def complexprefix(x):
    prefix, paths, sizes = x
    children = []
    for first, all in groupby(paths, itemgetter(0)):
        path = prefix + [first]
        shortened = [a[1:] for a in all if a[1:]]
        children.append((path, shortened, sizes))
    return None, children
def correct_sum_branch(node, children):
    assert(len(children)>0)
    path = children[0].node[0][:-1]
    for child in children:
        assert(child.node[0][:-1]==path)
    size = sum([child.node[1] for child in children])
    return (path, size)
def rawtree(f):
    sizes = {}
    for line in f:
        size, file = line.rstrip().split(None, 1)
        sizes[tuple(splitall(file))] = int(size)
    paths = list(sorted(sizes.keys()))
    leaves_only = morphisms.unspooltree3(
        issimple,
        simpleprefix,
        complexprefix,
        ([], paths, sizes), )
    full_tree = morphisms.treemap_with_benefits_bottomup(
        morphisms.identity,
        correct_sum_branch,
        leaves_only, )
    return full_tree

def xml(tree):
    return morphisms.reducetree(
            lambda leaf: '<file name="{0}" bytes="{1}"/>'.format('/'.join(leaf[0]), leaf[1]),
            lambda branch, leaves: '<dir name="{0}" bytes="{1}">{2}</dir>'.format('/'.join(branch[0]), branch[1], ''.join(leaves)),
            tree)

if __name__=='__main__':
    import fileinput
    x = xml(rawtree(fileinput.input()))
    print(x)
