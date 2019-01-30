# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        """my evaluation function calculates manhattan distance to the closest food, 
        how many ghosts can be eaten by pacman theoretically (using manhattan distance, not considering walls)
        and how many ghosts can eat pacman on the next step, for successor state; 
        multiplies them by coefficients of my choosing,
        based on their importance and adds them all to score of successor state"""

        ev = 0.0 + successorGameState.getScore()
        minFoodDist = 10000
        for (x, y) in newFood.asList():
            minFoodDist = min(minFoodDist, abs(newPos[0] - x) + abs(newPos[1] - y))
        # the closer the food is, the bigger value evaluation function should return
        ev += 1.25/minFoodDist  # coefficient is small, because it's not very important

        for i in xrange(len(newGhostStates)):
            manDistToGhost = abs(newGhostStates[i].getPosition()[0] - newPos[0]) + \
                             abs(newGhostStates[i].getPosition()[1] - newPos[1])
            if newScaredTimes[i] >= manDistToGhost:  # if pacman can eat i-th ghost
                ev += 400  # eating ghosts increases pacman's score significantly, so coefficient per ghost is big
            elif manDistToGhost == 1:
                ev -= 1000  # getting eaten by a ghost is very very bad, so coefficient is very high

        return ev

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    """minimizer function for minimax algorithm (these trees have one min layer for each ghost)
    depth parameter is the depth currently reached and index is the index of current agent"""
    def min_value(self, state, depth, index):
        actions = state.getLegalActions(index)
        if len(actions) == 0:  # height of the tree is less than requested depth
            return self.evaluationFunction(state)

        v = float('inf')
        for action in actions:
            succ = state.generateSuccessor(index, action)  # successor state
            if index < state.getNumAgents() - 1:  # if not the last ghost, take minimum of child minimizers
                v = min(v, self.min_value(succ, depth, index + 1))
            else:  # if last ghost (next is pacman's move), take minimum from child maximizers
                v = min(v, self.max_value(succ, depth + 1))
        return v

    """maximizer function for minimax algorithm
    depth parameter is the depth currently reached"""
    def max_value(self, state, depth):
        actions = state.getLegalActions(0)

        # if reached requested depth or height of the tree is less than requested depth, should return value
        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)

        v = float('-inf')
        for action in actions:
            succ = state.generateSuccessor(0, action)  # successor state
            v = max(v, self.min_value(succ, depth, 1))  # take maximum from child minimizers
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        """first node is maximizer, because first moves pacman"""
        action = Directions.WEST  # initializing action to return
        v = float('-inf')
        for a in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, a)
            minVal = self.min_value(succ, 0, 1)  # value of child minimizer
            if minVal > v:  # if found better action, store it in variable action
                v = minVal
                action = a
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)

      this is the same code as in normal minimax algorithm with alpha-beta pruning added
    """

    """argument a is max's best option on path to root
    and b is min's best option on path to root"""
    def min_value(self, state, depth, index, a, b):
        actions = state.getLegalActions(index)
        if len(actions) == 0:
            return self.evaluationFunction(state)

        v = float('inf')
        for action in actions:
            succ = state.generateSuccessor(index, action)
            if index < state.getNumAgents() - 1:
                v = min(v, self.min_value(succ, depth, index + 1, a, b))
            else:
                v = min(v, self.max_value(succ, depth + 1, a, b))
            if v < a:  # if minimizer's value is less than max's best option so far, no need to continue
                return v

            b = min(b, v)  # update b if found better option for minimizer
        return v

    def max_value(self, state, depth, a, b):
        actions = state.getLegalActions(0)

        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)

        v = float('-inf')
        for action in actions:
            succ = state.generateSuccessor(0, action)
            v = max(v, self.min_value(succ, depth, 1, a, b))
            if v > b:  # if maximizer's value is greater than min's best option so far, no need to continue
                return v

            a = max(a, v)  # update a if found better option for maximizer
        return v

    def getAction(self, gameState):
        action = Directions.WEST
        v = float('-inf')
        alpha = float('-inf')  # initially max's best option is negative infinity
        beta = float('inf')  # initially min's best option is infinity
        for a in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, a)
            minVal = self.min_value(succ, 0, 1, alpha, beta)
            if minVal > v:
                v = minVal
                action = a
            if v > beta:  # if maximizer's value is greater than min's best option so far, no need to continue
                return action

            alpha = max(alpha, v)  # update alpha if found better option for maximizer
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)

      everything's the same as in standard minimax algorithm, bust instead of minimizers,
      there are expected value counters
    """

    def expect_value(self, state, depth, index):
        actions = state.getLegalActions(index)
        if len(actions) == 0:
            return self.evaluationFunction(state)

        v = 0.0
        for action in actions:
            succ = state.generateSuccessor(index, action)
            if index < state.getNumAgents() - 1:  # child is also expected value counter
                # increase v by value of child multiplied by its probability
                v += self.expect_value(succ, depth, index + 1) / len(actions)
            else:  # child is maximizer
                # increase v by value of child multiplied by its probability
                v += self.max_value(succ, depth + 1) / len(actions)
        return v

    def max_value(self, state, depth):
        actions = state.getLegalActions(0)

        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)

        v = float('-inf')
        for action in actions:
            succ = state.generateSuccessor(0, action)
            v = max(v, self.expect_value(succ, depth, 1))
        return v

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        action = Directions.WEST
        v = float('-inf')
        for a in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, a)
            minVal = self.expect_value(succ, 0, 1)
            if minVal > v:
                v = minVal
                action = a
        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: it's the same as my reflex agent evaluation function,
      but instead of calculating everything for successor state,
      this time I calculate everything for current game state
    """
    food = currentGameState.getFood()
    pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    ev = 0.0 + currentGameState.getScore()
    minFoodDist = 10000
    for (x, y) in food.asList():
        minFoodDist = min(minFoodDist, abs(pos[0] - x) + abs(pos[1] - y))
    ev += 1.25 / minFoodDist
    for i in xrange(len(ghostStates)):
        manDistToGhost = abs(ghostStates[i].getPosition()[0] - pos[0]) + \
                         abs(ghostStates[i].getPosition()[1] - pos[1])
        if scaredTimes[i] >= manDistToGhost:
            ev += 400
        elif manDistToGhost == 1:
            ev -= 1000

    return ev

# Abbreviation
better = betterEvaluationFunction

