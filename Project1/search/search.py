# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    """in dfs we use a stack for storing paths needed to be considered
    paths are stored the following way: a list of actions needed to reach this position
    followed by current position (tuple of coordinates)
    all the other search algorithms are implemented the same way, with minor changes because of algorithm specifics"""
    toCons = util.Stack()
    toCons.push([problem.getStartState()])
    visited = []  # list of already visited locations we don't want to revisit
    path = []  # list I'm going to store answer (actions to reach goal state) in
    while not toCons.isEmpty():  # while there are paths to consider
        curr = toCons.pop()
        if curr[-1] not in visited:  # we don't want to visit same position more than once
            if problem.isGoalState(curr[-1]):  # reached goal state, no need to continue searching
                path = curr
                break
            for succ in problem.getSuccessors(curr[-1]):  # we must consider all neighbours of current position
                tmp = curr[:]  # copy current list of actions and position
                del tmp[-1]  # delete the position, because we need to add new action and update it with new position
                tmp.append(succ[1])  # append action needed to get to the new position at the end of the list
                tmp.append(succ[0])  # append new position to the end of the list
                toCons.push(tmp)  # push new path to the paths needed to be considered
            visited.append(curr[-1])  # this position is already visited
    del path[-1]  # we don't need the goal state position to be in answer so I delete it from the list
    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    """in bfs we use a queue for storing paths needed to be considered 
    everything else is the same as in dfs"""
    toCons = util.Queue()
    toCons.push([problem.getStartState()])
    visited = []
    path = []
    while not toCons.isEmpty():
        curr = toCons.pop()
        if curr[-1] not in visited:
            if problem.isGoalState(curr[-1]):
                path = curr
                break
            for succ in problem.getSuccessors(curr[-1]):
                tmp = curr[:]
                del tmp[-1]
                tmp.append(succ[1])
                tmp.append(succ[0])
                toCons.push(tmp)
            visited.append(curr[-1])
    del path[-1]
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    """in ucs we use a priority queue for storing paths needed to be considered
    in ucs we need to also store total costs of each path
    so, in paths I store in the priority queue, I also store this total costs, right before the position tuple"""
    toCons = util.PriorityQueue()
    toCons.push([0, problem.getStartState()], 0)  # total cost and also priority of starting state is 0
    visited = []
    path = []
    while not toCons.isEmpty():
        curr = toCons.pop()
        if curr[-1] not in visited:
            if problem.isGoalState(curr[-1]):
                path = curr
                break
            for succ in problem.getSuccessors(curr[-1]):
                tmp = curr[:]
                dist = tmp[-2] + succ[2]  # calculate total cost of new path, using cost of current path
                del tmp[-2:]  # new action should be added and cost and position should be updated
                tmp.append(succ[1])  # append new action
                tmp.append(dist)  # append total cost
                tmp.append(succ[0])  # append new position
                toCons.push(tmp, dist)  # priority of this path will be its total cost
            visited.append(curr[-1])
    del path[-2:]  # we don't need the goal position, as well as cost to be in answer so I delete them from the list
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """in A* search we use a priority queue for storing paths needed to be considered
    in fact, everything is the same as in ucs, but priorities are cost + heuristic, instead of just cost"""
    toCons = util.PriorityQueue()
    # priority of start state is heuristic from start state and cost is 0
    toCons.push([0, problem.getStartState()], heuristic(problem.getStartState(), problem))
    visited = []
    path = []
    while not toCons.isEmpty():
        curr = toCons.pop()
        if curr[-1] not in visited:
            if problem.isGoalState(curr[-1]):
                path = curr
                break
            for succ in problem.getSuccessors(curr[-1]):
                tmp = curr[:]
                dist = tmp[-2] + succ[2]
                del tmp[-2:]
                tmp.append(succ[1])
                tmp.append(dist)
                tmp.append(succ[0])
                toCons.push(tmp, dist + heuristic(succ[0], problem))  # priority is cost + heuristic
            visited.append(curr[-1])
    del path[-2:]
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
