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
import numpy as np

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
        distance = manhattanDistance(newPos, newGhostStates[0].getPosition())

        "[Project 3] YOUR CODE HERE"

        # print "action", action
        # print "successorGameState\n", successorGameState
        # print "newPos", newPos
        # print "newFood\n", newFood
        # print "newLen", newFood.width, newFood.height
        # print "newGhostPosition", newGhostStates[0].getPosition()
        # print "newScaredTimes", newScaredTimes
        # print "distance", distance
        # print ""

        def circleFoodScore(newPos, newFood):
            """
            newFood: grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
            y vertical and the origin (0,0) in the bottom left corner
            wall will take col 0 and col 24, row 0 and row 8
            """
            score = 0
            left = newPos[0]-1 if newPos[0]-1>=0 else 0
            right = newPos[0]+1 if newPos[0]+1<newFood.width else newFood.width-1
            top = newPos[1]-1 if newPos[1]-1>=0 else 0
            bottom = newPos[1]+1 if newPos[1]+1<newFood.height else newFood.height-1
            print left, right, top, bottom
            print newFood[top:bottom+1][left:right+1]

        if distance < 2:
            return -2147483647
        elif distance < 3:
            return -2147483646
        elif successorGameState.getScore() - currentGameState.getScore() > 0:
            return successorGameState.getScore()
        elif action == Directions.STOP:
            return -2147483645
        else:
            score = 0
            for i in range(newFood.width):
                for j in range(newFood.height):
                    if newFood[i][j]:
                        score -= abs(newPos[0] - i) + abs(newPos[1] - j)
                    else:
                        score -= 256
            return score

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

        "[Project 3] YOUR CODE HERE"

        def minimax(gameState, cdepth, linkDict):
            agentIndex = cdepth%gameState.getNumAgents()
            legalActions = gameState.getLegalActions(agentIndex)
            """The meaning of depth is that you must go until (self.depth+1)'s max layer"""
            if gameState.isLose() or gameState.isWin() or len(legalActions)==0 or cdepth==self.depth*gameState.getNumAgents():
                return self.evaluationFunction(gameState)
            elif agentIndex==0:
                successors = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
                successors_scores = [minimax(successor, cdepth+1, linkDict) for successor in successors]
                successors_scores = np.asarray(successors_scores)
                maxid = successors_scores.argmax()
                linkDict.update({gameState:legalActions[maxid]})
                return max(successors_scores)
            else:
                successors = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
                successors_scores = [minimax(successor, cdepth+1, linkDict) for successor in successors]
                successors_scores = np.asarray(successors_scores)
                minid = successors_scores.argmin()
                linkDict.update({gameState:legalActions[minid]})
                return min(successors_scores)

        linkDict = {}
        minimax(gameState, 0, linkDict)
        path = []
        cState = gameState
        for i in range(self.depth):
            agentIndex = i%gameState.getNumAgents()
            if cState in linkDict.keys():
                if agentIndex==0: path.append(linkDict[cState])
                cState = cState.generateSuccessor(agentIndex, linkDict[cState])
        return path[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        "[Project 3] YOUR CODE HERE"

        def alphabetapruning(gameState, cdepth, linkDict, alpha, beta):
            agentIndex = cdepth%gameState.getNumAgents()
            legalActions = gameState.getLegalActions(agentIndex)
            """The meaning of depth is that you must go until (self.depth+1)'s max layer"""
            if gameState.isLose() or gameState.isWin() or len(legalActions)==0 or cdepth==self.depth*gameState.getNumAgents(): #cdepth==self.depth:
                return self.evaluationFunction(gameState)
            elif agentIndex==0:
                v = -float("inf")
                bestAction = None
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)
                    score = alphabetapruning(successor, cdepth+1, linkDict, alpha, beta)
                    if score > v:
                        v = score
                        bestAction = action
                    if v > beta: #don't use >=
                        linkDict.update({gameState:action})
                        return v
                    alpha = max(alpha,v) #the sibling will get a new alpha
                linkDict.update({gameState:bestAction})
                return v
            else:
                v = float("inf")
                bestAction = None
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)
                    score = alphabetapruning(successor, cdepth+1, linkDict, alpha, beta)
                    if score < v:
                        v = score
                        bestAction = action
                    if v < alpha: #don't use <=
                        linkDict.update({gameState:action})
                        return v
                    beta = min(beta,v)
                linkDict.update({gameState:bestAction})
                return v

        alpha = -float("inf")
        beta = float("inf")
        linkDict = {}
        alphabetapruning(gameState, 0, linkDict, alpha, beta)
        path = []
        cState = gameState
        for i in range(self.depth):
            agentIndex = i%gameState.getNumAgents()
            if cState in linkDict.keys():
                if agentIndex==0: path.append(linkDict[cState])
                cState = cState.generateSuccessor(agentIndex, linkDict[cState])
        return path[0]

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """

    "[Project 3] YOUR CODE HERE"

    return currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
