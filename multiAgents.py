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
"""Sarah Harkin and Monica Bebawy"""

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
        # This is your code. 
        foodList = newFood.asList()
        eFunction = 0
        for food in foodList:
            for ghostState in newGhostStates:
                foodToPacman = util.manhattanDistance(newPos, food)
            
        
                ghostPos = ghostState.getPosition()
                ghostToPacman = util.manhattanDistance(newPos, ghostPos)
        
                eFunction = ( 5  * 1/foodToPacman) + (6 * ghostToPacman)
                return  eFunction
        return successorGameState.getScore()

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
        def value (gameState, agentIndex, depth):
            if agentIndex == gameState.getNumAgents():
                depth = depth -1
                agentIndex = 0
            if gameState.isLose() or gameState.isWin() or depth == 0:
                return self.evaluationFunction(gameState)
            elif agentIndex == 0:
                return maxValue(gameState, agentIndex, depth )
            elif agentIndex != 0:
                return minValue(gameState, agentIndex, depth)
        def maxValue(gameState, agentIndex, depth):
            v = float ('-inf')
            #for successor in gameState.generateSuccessor(index, action):
            legalActions = gameState.getLegalActions(agentIndex)
            #evaluate each possible action for PACMAN
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = max(v,value(successor, agentIndex+1, depth))
            #index += 1
            return v
        def minValue(gameState, agentIndex, depth):
            v = float ('inf')
            #for successor in gameState.generateSuccessor(index, action):
            legalActions = gameState.getLegalActions(agentIndex)
            #evaluate each possible action for PACMAN
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = min(v,value(successor, agentIndex+1, depth))
            #index += 1
            return v
        agentIndex = 0
        maxScore = -100000000
        bestAction = "NA"
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor (0, action)
            score = value(successor, agentIndex+1, self.depth)
            if score > maxScore:
                maxScore = score
                bestAction = action
        return bestAction
        
       
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = float('-inf')
        b = float('inf')
        def value (gameState, agentIndex, depth, a, b):
            if agentIndex == gameState.getNumAgents():
                depth = depth -1
                agentIndex = 0
            if gameState.isLose() or gameState.isWin() or depth == 0:
                return self.evaluationFunction(gameState)
            elif agentIndex == 0:
                return maxValue(gameState, agentIndex, depth, a, b )
            elif agentIndex != 0:
                return minValue(gameState, agentIndex, depth, a, b)
        def maxValue(gameState, agentIndex, depth,a,b):
            v = float ('-inf')
            #for successor in gameState.generateSuccessor(index, action):
            legalActions = gameState.getLegalActions(agentIndex)
            #evaluate each possible action for PACMAN
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = max(v,value(successor, agentIndex+1, depth,a,b))
                if v>= b:
                    return v
                a = max(a,v)
            #index += 1
            return v
        def minValue(gameState, agentIndex, depth,a,b):
            v = float ('inf')
            #for successor in gameState.generateSuccessor(index, action):
            legalActions = gameState.getLegalActions(agentIndex)
            #evaluate each possible action for PACMAN
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = min(v,value(successor, agentIndex+1, depth,a,b))
                if v <= a:
                    return v
                b = min(b,v)
            #index += 1
            return v
        agentIndex = 0
        maxScore = -100000000
        bestAction = "NA"
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor (0, action)
            score = value(successor, agentIndex+1, self.depth,a,b)
            if score > maxScore:
                maxScore = score
                bestAction = action
        return bestAction
        #util.raiseNotDefined()

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
        def value (gameState, agentIndex, depth):
            if agentIndex == gameState.getNumAgents():
                depth = depth -1
                agentIndex = 0
            if gameState.isLose() or gameState.isWin() or depth == 0:
                return self.evaluationFunction(gameState)
            elif agentIndex == 0:
                return maxValue(gameState, agentIndex, depth )
            elif agentIndex != 0:
                return expValue(gameState, agentIndex, depth)
        def maxValue(gameState, agentIndex, depth):
            v = float ('-inf')
            #for successor in gameState.generateSuccessor(index, action):
            legalActions = gameState.getLegalActions(agentIndex)
            #evaluate each possible action for PACMAN
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = max(v,value(successor, agentIndex+1, depth))
            #index += 1
            return v
        def expValue(gameState, agentIndex, depth):
            v = 0
            #for successor in gameState.generateSuccessor(index, action):
            legalActions = gameState.getLegalActions(agentIndex)
            #evaluate each possible action for PACMAN
            countAction = 0
            for action in legalActions:
                countAction += 1
            for action in legalActions:    
                successor = gameState.generateSuccessor(agentIndex, action)
                p = float (1.0/countAction) 
                #value = float (value(gameState, agentIndex, depth))
                v += p * float (value(successor, agentIndex+1, depth))

            #index += 1
            return v
        agentIndex = 0
        maxScore = -100000000
        bestAction = "NA"
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor (0, action)
            score = value(successor, agentIndex+1, self.depth)
            if score > maxScore:
                maxScore = score
                bestAction = action
        return bestAction
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      
      in this function we are trying to have a better evaluation for pacman 
      first: we need to see if the ghosts are scared or not. If the ghosts are scared, we find
      the distance from the ghost to pacman is and if it is less than the value of the scared time pacman ignores it
      but if the value is grater than the number of moves to the ghosts, then pacman chases the ghost. 
    """

    "*** YOUR CODE HERE ***"
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # This is your code. 
    foodList = newFood.asList()
    eFunction = 0
    ghost = 0
    for food in foodList:
        for ghostState in newGhostStates:
            
            foodToPacman = util.manhattanDistance(newPos, food)   
            ghostPos = ghostState.getPosition()
            ghostToPacman = util.manhattanDistance(newPos, ghostPos)
            
            value = newScaredTimes[ghost]
            ghost += 1
            if value >= ghostToPacman and ghostToPacman != 0:
                eFunction = ( 5  * 1/foodToPacman) + (5 * 1/ghostToPacman) 
            elif value < ghostToPacman and ghostToPacman != 0:
                eFunction =   (2 * ghostToPacman) + ( 15  * 1/foodToPacman)
            return  eFunction
    return currentGameState.getScore()

    #util.raiseNotDefined()
    
# Abbreviation
better = betterEvaluationFunction

