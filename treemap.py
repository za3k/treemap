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
def rawtree():
    sizes = {}
    with open("rawdata") as f:
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

def color(n):
    colors = list(map(lambda x: "rgb{0}".format(str(x)),
            [(20, 0, 0), (0, 255, 0), (0, 0, 255),
             (255, 255, 0), (255, 0, 255), (0, 255, 255)]))
    return colors[n % len(colors)]
def even(n):
    return (n%2)==0
def rectangles(sizetree, parent, depth=0):
    parent.color = color(depth)
    if isinstance(sizetree, morphisms.Branch):
        children = sizetree.branches
        scaled = scale([child.node[1] for child in children])
        hborder,vborder = 0.1*parent.width, 0.1*parent.height
        bordered = Rectangle(top=parent.top+vborder/2, bottom=parent.bottom-vborder/2, left=parent.left+hborder/2, right=parent.right-hborder/2)
        if even(depth):
            subrects = bordered.split_horiz(*scaled)
        else:
            subrects = bordered.split_vert(*scaled)
        subrects = list(subrects)

        rects = []
        for subrect, child in zip(subrects, children):
            sr = rectangles(child, subrect, depth+1)
            rects += sr
        return [parent] + rects
    elif isinstance(sizetree, morphisms.Leaf):
        return [parent]
    assert(False)

class Rectangle():
    def  __init__(self, top, bottom, left, right, color="rgb(200,0,0)"):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.color = color
    def split_horiz(self,*scaled_sizes):
        end_positions = list(accumulate(scaled_sizes))
        assert(abs(end_positions[-1]-1) < 0.01)
        end_positions = end_positions[:-1]+[1]
        start_positions = [0]+end_positions[:-1]
        for begin, end in zip(start_positions, end_positions):
            yield(self.scaled_child(top=begin, bottom=end))
    def split_vert(self,*scaled_sizes):
        end_positions = list(accumulate(scaled_sizes))
        assert(abs(end_positions[-1]-1) < 0.01)
        end_positions = end_positions[:-1]+[1]
        start_positions = [0]+end_positions[:-1]
        for begin, end in zip(start_positions, end_positions):
            yield(self.scaled_child(left=begin, right=end))
    def scaled_child(self,left=0, right=1, top=0, bottom=1):
        assert(0<=left<right<=1)
        assert(0<=top<bottom<=1)
        return Rectangle(left=left*self.width+self.left, right=right*self.width+self.left, top=top*self.height+self.top, bottom=bottom*self.height+self.top)
    @property
    def width(self):
        return self.right-self.left
    @property
    def height(self):
        return self.bottom-self.top

def drawable_poly(p, color="rgb(200,0,0)"):
    return {"points":p, "fill":color}
def drawable_rect(r):
    # Clockwise - see if this is right
    return drawable_poly([[r.left, r.top], [r.right, r.top], [r.right, r.bottom], [r.left, r.bottom],], color=r.color)
def drawable_rects(rs):
    return list(map(drawable_rect, rs))
def draw(rectangles):
    with open("ZaksTreeMap.html") as f:
        d = f.read()
    print(d.replace("INSERTDATAHERE", json.dumps(drawable_rects(rectangles))))
    #print(drawable_rects(rectangles))

def scale(relative_sizes):
    total = sum(relative_sizes)
    scaled = [size/total for size in relative_sizes]
    return scaled

if __name__=='__main__':
    input = rawtree()
    alternating_layout = input
    #pprint(input)
    #draw([Rectangle(top=.3, bottom=.9, left=.1, right=.9)])
    draw(rectangles(alternating_layout, Rectangle(top=.1, bottom=.9, left=.1, right=.9, color="transparent")))
