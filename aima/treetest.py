'''
Tests tree-search algorithms search by seeking goal nodes in a  fully balanced binary tree.  Each 
node is assigned a random cost, and is set to be a goal node with a specified probability.  
Includes a TreeProblem class, implementing the methods defined in the Problem API.

Usage:

   python treetest.py <depth> <goalprob> [seed]

Examples:

   python treetest.py 3 0.2

   python treetest.py 4 0.1 0
'''

MAXCOST = 100	

import sys
import random

#from dfsearch import DFSearch
#from bfsearch import BFSearch
#from ucsearch import
from problem import Problem
from search import breadth_first_search

class TreeProblem(Problem):
	
# methods exported to Search class ---------------------------------------------	
	 
    # initial "state" of a tree is just its root	
    def initialState(self):
	return self.root.id
	
    # goal test is whether goal matches node label
    def goal_test(self, state):
	node = self.nodes[state]
	return node.isgoal
	
    # successors of a node are its children
    def successorFn(self, state):
	node = self.nodes[state]
	if node.isTerminal():
	    return []
	else:
	    return [self._contents('l', node.lchild), \
	            self._contents('r', node.rchild)]
	    	   
    # step cost state--[action]-->result is just the random cost associated with result
    def stepCost(self, state, action, result):
	node = self.nodes[result]
	return node.cost
	
    # no action is actually taken; we just print out the state for debugging	
    def takeActions(self, state): 
	return 'visit ', state
	

# other public methods ---------------------------------------------------------	
	
     # creates a fully-balanced binary tree of specified depth, with goals
     # at randomly-chosen nodes.  Step costs are also random.
    def __init__(self, depth, goalprob):

	# root has id 0, has no cost or pathcost, is not goal
        self.initial = 0;
        self.goal = None
        self.root = BTree(0, 0, 0, False); 
	 
	self.nodes = [self.root]
	
	while self.root.depth() < depth:
	    self.root.expandFringe(goalprob, self.nodes)
	     	     	 
	
    # enables string representation of tree for debugging with print	
    def __str__(self):
	return self._str_helper(self.root, '')
	
# private methods --------------------------------------------------------------

    def _contents(self, label, node):
	return (label, node.id)
	    
    def _str_helper(self, node, indent):
	s = indent + str(node)
	if not node.isTerminal():
	    s = s + '\n' + self._str_helper(node.lchild, indent + '  ')
	    s = s + '\n' + self._str_helper(node.rchild, indent + '  ')
	return s

# local class for binary-tree nodes---------------------------------------------
	
class BTree:

    def __init__(self, id, cost, pathcost, isgoal):
        self.lchild = None
	self.rchild = None
	self.id = id
	self.cost = cost
        self.pathcost = pathcost	
	self.isgoal = isgoal
	
    def __repr__(self):
	s = str(self.id)
	if self.isgoal:
	    s += '*'
	s = s + ': ' + str(self.cost) + ',' + str(self.pathcost)    
	return s
	
	
    def depth(self):
	if self.isTerminal():
	    return 0
	else:
	    return 1 + max(self.lchild.depth(), self.rchild.depth())
	    
    def expandFringe(self, goalprob, nodes):
	fringe = self.getFringe()
	id = fringe[len(fringe)-1].id
	for node in fringe:
	    node.lchild = self._new_node(node, id, 1, goalprob, nodes)
	    node.rchild = self._new_node(node, id, 2, goalprob, nodes)
	    id += 2
	    
    def getFringe(self):
	fringe = []
	self._getFringe(fringe)
	return fringe
	
	
    def isTerminal(self):
	return self.lchild == None
	
    def getCost(self):
	return self.cost
		
    def _new_node(self, parent, id, offset, goalprob, nodes):	
	cost = random.randint(1,MAXCOST)
	pathcost = cost + parent.pathcost
	isgoal = random.random()<goalprob
        node = BTree(id+offset, cost, pathcost, isgoal)
        nodes.append(node)
        return node
	    
    def _getFringe(self, fringe):
        if self.isTerminal():
	    fringe.append(self)
	else:
	    self.lchild._getFringe(fringe)
	    self.rchild._getFringe(fringe)
	
# main ------------------------------------------------------------------------

# bozo filter
if len(sys.argv) < 3:
    print 'Usage: python treetest.py <depth> <goalprob> [seed]'
    sys.exit() 

# get params from command line
depth  = int(sys.argv[1])
goalprob = float(sys.argv[2])

# get optional random seed for reproducibility
if len(sys.argv) > 3:
    random.seed(int(sys.argv[3]))

# build fbb tree problem with specified depth, goal
problem = TreeProblem(depth, goalprob)

# show the tree for debugging
print 'Format: state(*=goal): stepcost, pathcost'
print problem

# search for the goal depth-first, breadth-first, and by uniform cost
#print 'DFS:'
#s = DFSearch()
#print search.depth_limited_search(problem)
#print '\nBFS:'
#s = BFSearch()
print breadth_first_search(problem)
#print '\nUCS:'
#s = UCSearch()
#print search.uniform_cost_search(problem)
