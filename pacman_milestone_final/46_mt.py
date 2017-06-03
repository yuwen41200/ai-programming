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
    isRed = True
    history = [
        Directions.STOP,
        Directions.STOP,
        Directions.STOP,
        Directions.STOP
    ]

    def registerInitialState(self, gameState):

        CaptureAgent.registerInitialState(self, gameState)
        self.isRed = gameState.isOnRedTeam(self.index[0])

    def chooseAction(self, gameState):

        try:

            actions = gameState.getLegalActions(self.index[0])

            values = [self.evaluate(gameState, action) for action in actions]
            maxValue = max(values)
            bestActions = [action for action, value in zip(actions, values) if value == maxValue]

            chosenAction = choice(bestActions)
            self.history.append(chosenAction)
            if (
                self.history[-1] == self.history[-3] and
                self.history[-2] == self.history[-4] and
                self.history[-1] == Directions.REVERSE[self.history[-2]]
            ):
                newActions = [action for action in actions if action != chosenAction]
                chosenAction = choice(newActions)
                self.history[-1] = chosenAction

            self.history = self.history[-4:]
            return self.history[-1]

        except Exception:

            if Directions.SOUTH in gameState.getLegalActions(self.index[0]):
                return Directions.SOUTH
            else:
                return Directions.STOP

    def evaluate(self, gameState, action):

        successor = gameState.generateSuccessor(self.index[0], action)
        pos = successor.getAgentState(self.index[0]).getPosition()
        foods = self.getFood(successor).asListNot()
        capsules = self.getCapsules(successor)
        if self.isRed:
            gpos1 = successor.getAgentState(5).getPosition()
            gpos2 = successor.getAgentState(7).getPosition()
        else:
            gpos1 = successor.getAgentState(4).getPosition()
            gpos2 = successor.getAgentState(6).getPosition()
        dis1 = self.distancer.getDistance(pos, gpos1)
        dis2 = self.distancer.getDistance(pos, gpos2)

        score = successor.getScore()
        if not self.isRed:
            score = -score
        for food in foods:
            score -= self.distancer.getDistance(pos, food)
        for capsule in capsules:
            score -= 10 * self.distancer.getDistance(pos, capsule)
        score += dis1
        score += dis2
        if action == Directions.STOP:
            score -= 10000
        if (pos[0]+1, pos[1]) in foods or (pos[0]-1, pos[1]) in foods:
            score += 100
        if (pos[0], pos[1]+1) in foods or (pos[0], pos[1]-1) in foods:
            score += 100
        if dis1 <= 1 or dis2 <= 1:
            score -= 100000

        print self.no, action, pos, score
        return score

class ReflexAgent0(ReflexAgent):

    no = 0

class ReflexAgent1(ReflexAgent):

    no = 1

    def chooseAction(self, gameState):

        try:

            actions = gameState.getLegalActions(self.index[1])

            values = [self.evaluate(gameState, action) for action in actions]
            maxValue = max(values)
            bestActions = [action for action, value in zip(actions, values) if value == maxValue]

            return choice(bestActions)

        except Exception:

            if Directions.SOUTH in gameState.getLegalActions(self.index[1]):
                return Directions.SOUTH
            else:
                return Directions.STOP

    def evaluate(self, gameState, action):

        successor = gameState.generateSuccessor(self.index[1], action)
        pos = successor.getAgentState(self.index[1]).getPosition()
        if self.isRed:
            ppos1 = successor.getAgentState(1).getPosition()
            ppos2 = successor.getAgentState(3).getPosition()
        else:
            ppos1 = successor.getAgentState(0).getPosition()
            ppos2 = successor.getAgentState(2).getPosition()

        dis = min(self.distancer.getDistance(pos, ppos1), self.distancer.getDistance(pos, ppos2))
        score = successor.getScore()
        if not self.isRed:
            score = -score
        score -= dis

        print self.no, action, pos, score
        return score
