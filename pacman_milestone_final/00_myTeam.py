# myTeam.py
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

from captureAgents import CaptureAgent
from game import Directions
from random import choice

#################
# Team creation #
#################

def createTeam(indexes, num, isRed, names=['ReflexAgent0', 'ReflexAgent1']):
    """
    This function should return a list of agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.    isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments, which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """

    # The following line is an example only; feel free to change it.
    return [eval(name)(index) for name, index in zip(names, indexes)]

##########
# Agents #
##########

class ReflexAgent(CaptureAgent):

    no = -1

    def registerInitialState(self, gameState):

        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):

        actions = gameState.getLegalActions(self.index[0])

        values = [self.evaluate(gameState, action) for action in actions]
        maxValue = max(values)
        bestActions = [action for action, value in zip(actions, values) if value == maxValue]

        return choice(bestActions)

    def evaluate(self, gameState, action):

        successor = gameState.generateSuccessor(self.index[0], action)
        pos = successor.getAgentState(self.index[0]).getPosition()
        foods = self.getFood(successor).asListNot()
        capsules = self.getCapsules(successor)
        gpos1 = successor.getAgentState(5).getPosition()
        gpos2 = successor.getAgentState(7).getPosition()

        score = successor.getScore()
        for food in foods:
            score -= self.distancer.getDistance(pos, food)
        for capsule in capsules:
            score -= 10 * self.distancer.getDistance(pos, capsule)
        score += self.distancer.getDistance(pos, gpos1)
        score += self.distancer.getDistance(pos, gpos2)
        if action == Directions.STOP:
            score -= 10000

        print self.no, action, pos, score
        return score

class ReflexAgent0(ReflexAgent):

    no = 0

class ReflexAgent1(ReflexAgent):

    no = 1

    def evaluate(self, gameState, action):

        successor = gameState.generateSuccessor(self.index[1], action)
        pos = successor.getAgentState(self.index[1]).getPosition()
        ppos1 = successor.getAgentState(1).getPosition()

        score = successor.getScore()
        score -= self.distancer.getDistance(pos, ppos1)
        if action == Directions.STOP:
            score -= 10000

        print self.no, action, pos, score
        return score
