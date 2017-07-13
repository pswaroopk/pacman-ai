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

        "*** YOUR CODE HERE ***"
        distance = []
        foodList = currentGameState.getFood().asList()
        infinity = float("inf")#huge negative Val. dont take this positon
        currPos = currentGameState.getPacmanPosition()

        if successorGameState.isWin():
            return infinity
        elif newPos == currPos or action == 'Stop':
            return -infinity
        else:
            for ghostState in newGhostStates:
                if manhattanDistance(ghostState.getPosition(), newPos) < 2 and ghostState.scaredTimer is 0:
                    return -infinity
                elif ghostState.scaredTimer > 4:#this is test
                    distance.append(-manhattanDistance(ghostState.getPosition(), newPos))
        for foodPos in foodList:
            distance.append(-manhattanDistance(foodPos, newPos))
        return max(distance)

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

    # agents = []
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction."""
        "*** YOUR CODE HERE ***"

        value = -float("inf")
        bestMove = []
        self.agents = range(gameState.getNumAgents())
        successors = [(action, gameState.generateSuccessor(0, action)) for action in gameState.getLegalActions(0)]
        for successor in successors:
            newValue = self.minimax(successor[1], 0, 1)
            bestMove, value = (successor[0], newValue) if newValue > value else (bestMove, value)
        return bestMove

    def minimax(self, state, depth, agent):
        agent, depth = (0, depth+1) if agent >= len(self.agents) else (agent, depth)
        if depth == self.depth or state.isWin() == True or state.isLose() == True:
            return self.evaluationFunction(state)
        value = -float("inf") if agent == 0 else float("inf")
        for action in state.getLegalActions(agent):
            if agent == 0:
                value = max(self.minimax(state.generateSuccessor(agent, action), depth, agent+1), value)
            else:
                value = min(self.minimax(state.generateSuccessor(agent, action), depth, agent+1), value)
        return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        bestMove = []
        self.agents = range(gameState.getNumAgents())
        successors = [(action, gameState.generateSuccessor(0, action)) for action in gameState.getLegalActions(0)]
        for successor in successors:
            newValue = self.alphaBetaPrune(successor[1], 0, 1, alpha, beta)
            bestMove, value = (successor[0], newValue) if newValue > value else (bestMove, value)
            if value >= beta:
                return bestMove
            alpha = max(alpha, value)
        return bestMove

    def alphaBetaPrune(self, state, depth, agent, alpha, beta):
        agent, depth = (0, depth+1) if agent >= len(self.agents) else (agent, depth)
        if depth == self.depth or state.isWin() == True or state.isLose() == True:
            return self.evaluationFunction(state)

        value = -float("inf") if agent == 0 else float("inf")
        for action in state.getLegalActions(agent):
            if agent == 0:
                value = max(self.alphaBetaPrune(state.generateSuccessor(agent, action), depth, agent+1, alpha, beta), value)
                if value > beta:
                    return value
                alpha = max(alpha, value)
            else:
                value = min(self.alphaBetaPrune(state.generateSuccessor(agent, action), depth, agent+1, alpha, beta), value)
                if value < alpha:
                    return value
                beta = min(beta, value)
        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        value = -float("inf")
        bestMove = []
        self.agents = range(gameState.getNumAgents())
        successors = [(action, gameState.generateSuccessor(0, action)) for action in gameState.getLegalActions(0)]
        for successor in successors:
            newValue = self.expectimax(successor[1], 0, 1)
            bestMove, value = (successor[0], newValue) if newValue > value else (bestMove, value)
        return bestMove

    def expectimax(self, state, depth, agent):
        agent, depth = (0, depth+1) if agent >= len(self.agents) else (agent, depth)
        if depth == self.depth or state.isWin() == True or state.isLose() == True:
            return self.evaluationFunction(state)
        value = -float("inf") if agent == 0 else 0
        prob = 1.0/len(state.getLegalActions(agent))
        for action in state.getLegalActions(agent):
            if agent == 0:
                value = max(value, self.expectimax(state.generateSuccessor(agent, action), depth, agent+1))
            else:
                value += prob * (self.expectimax(state.generateSuccessor(agent, action), depth, agent+1))
        return value


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).
      DESCRIPTION: <write something here so we know what you did>
    """
    score, bMin = 0, 0
    pacPos = currentGameState.getPacmanPosition()
    mindist = float("inf")
    for foodPos in currentGameState.getFood().asList():
        bMin, mindist = (1, util.manhattanDistance(pacPos, foodPos)) if util.manhattanDistance(pacPos, foodPos) < mindist else (bMin, mindist)
    score = score + mindist if bMin is 1 else score
    score = score + 555*currentGameState.getNumFood() + 55*len(currentGameState.getCapsules()) - 5*currentGameState.getScore()
    for gPos in currentGameState.getGhostPositions():
        score = float("inf") if util.manhattanDistance(pacPos, gPos) < 2 else score
    return -score

# # Abbreviation
better = betterEvaluationFunction
