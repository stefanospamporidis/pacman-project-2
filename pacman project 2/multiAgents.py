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
        # print 'sucgamestate', successorGameState
        newPos = successorGameState.getPacmanPosition()
        # print 'newpos', newPos
        newFood = successorGameState.getFood()
        # print newFood.asList()
        newGhostStates = successorGameState.getGhostStates()
        # print 'newGhoststates', newGhostStates
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print 'newScaredTimes', newScaredTimes

        "*** YOUR CODE HERE ***"
        
        #to action einai i kinisi pou 8a kanei o pacman kai tin exw parei ws dedomeno
        if action=='Stop':
            return float("-Inf") # an i energeia einai stop epistrefoume tin mikroteri dunati timi tis python(-oo)

        for GhostState in newGhostStates:
            if GhostState.getPosition() == newPos and GhostState.scaredTimer ==0 :
                return float("-Inf")

        foodlist=currentGameState.getFood().asList()
        #briskoyme oles tis manhattanDistances apo to newPos kai epistrefoume thn megalyterh
        distlist = [-1 * (manhattanDistance(newPos,food)) for food in foodlist]
        
        return max(distlist)


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
        "*** YOUR CODE HERE ***"
        def Min_Value(gameState, agent, depth):
            ghostActions = gameState.getLegalActions(agent)
            minimum = ["noaction", float("inf")]

            for action in ghostActions:
                newState = gameState.generateSuccessor(agent, action)
                newVal = Minimax_Decision(newState, agent + 1, depth)

                if newVal[1] < minimum[1]:
                    minimum = [action, newVal[1]]
            return minimum

        def Max_Value(gameState, agent, depth):
            packmanActions = gameState.getLegalActions(agent)
            maximum = ["noaction", float("-inf")]

            for action in packmanActions:
                newState = gameState.generateSuccessor(agent, action)
                newVal = Minimax_Decision(newState, agent + 1, depth)

                if newVal[1] > maximum[1]:
                    maximum = [action, newVal[1]]
            return maximum


        def Minimax_Decision(gameState, agent, depth):
            if agent >= gameState.getNumAgents():
                depth += 1
                agent = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return ["finalaction", self.evaluationFunction(gameState)]
            elif (agent == 0):
                return Max_Value(gameState, agent, depth)
            else:
                return Min_Value(gameState, agent, depth)

        return Minimax_Decision(gameState, 0, 0)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def Min_Value(gameState, agent, depth,a,b):
            ghostActions = gameState.getLegalActions(agent)
            minimum = ["noaction", float("inf")]

            for action in ghostActions:
                newState = gameState.generateSuccessor(agent, action)
                newVal = Minimax_Decision(newState, agent + 1, depth, a, b)

                if newVal[1] < minimum[1]:
                    minimum = [action, newVal[1]]
                if newVal[1] < a:
                    return [action,newVal[1]]
                b = min(b,newVal[1])
            return minimum

        def Max_Value(gameState, agent, depth, a ,b):
            packmanActions = gameState.getLegalActions(agent)
            maximum = ["noaction", float("-inf")]

            for action in packmanActions:
                newState = gameState.generateSuccessor(agent, action)
                newVal = Minimax_Decision(newState, agent + 1, depth , a, b)

                if newVal[1] > maximum[1]:
                    maximum = [action, newVal[1]]
                if newVal[1] > b:
                    return [action,newVal[1]]
                a = max(a,newVal[1])
            return maximum


        def Minimax_Decision(gameState, agent, depth , a, b):
            if agent >= gameState.getNumAgents():
                depth += 1
                agent = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return ["finalaction", self.evaluationFunction(gameState)]
            elif (agent == 0):
                return Max_Value(gameState, agent, depth, a, b)
            else:
                return Min_Value(gameState, agent, depth, a, b)

        return Minimax_Decision(gameState, 0, 0, float("-inf"), float("inf"))[0]

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
        "*** YOUR CODE HERE ***"
        def ghostExpect(gameState, agent, depth):
            ghostActions = gameState.getLegalActions(agent)
            maxVal = ["noaction", 0]
            prob = 1.0 / len(ghostActions)
            
            for action in ghostActions:
                newState = gameState.generateSuccessor(agent, action)
                maxVal[0] = action
                maxVal[1] += (prob * expectimax(newState, agent + 1, depth)[1])

            return maxVal

        def packmanMaxValue(gameState, agent, depth):
            packmanActions = gameState.getLegalActions(agent)
            maxVal = ["noaction", float("-inf")]
            
            for action in packmanActions:
                newState = gameState.generateSuccessor(agent, action)
                newVal = expectimax(newState, agent + 1, depth)

                if newVal[1] > maxVal[1]:
                    maxVal = [action, newVal[1]]
            return maxVal

        def expectimax(gameState, agent, depth):
            if agent >= gameState.getNumAgents():
                depth += 1
                agent = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return ["finalaction", self.evaluationFunction(gameState)]
            elif (agent == 0):
                return packmanMaxValue(gameState, agent, depth)
            else:
                return ghostExpect(gameState, agent, depth)

        return expectimax(gameState, 0, 0)[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacpos = currentGameState.getPacmanPosition()
    foodlist = currentGameState.getFood().asList()

    foods = [-1 * manhattanDistance(pacpos, food) for food in foodlist]

    if foods == []:
        foods = [0]

    return max(foods) + currentGameState.getScore()




    
    
# Abbreviation
better = betterEvaluationFunction









