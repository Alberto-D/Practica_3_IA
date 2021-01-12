# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A=logic.Expr('A')
    B=logic.Expr('B')
    C=logic.Expr('C')
    First= A | B
    Second= ~A % (~B | C)
    Third= logic.disjoin((~A), (~B), C) 

    Final2 = logic.conjoin(First, Second, Third)
    return Final2
    #util.raiseNotDefined()

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A=logic.Expr('A')
    B=logic.Expr('B')
    C=logic.Expr('C')
    D=logic.Expr('D')

    First= C % (B | D)
    Second= A >> (~B & ~D)
    Third= ~(B & ~C) >> A
    Forth= ~D>>C


    Final = logic.conjoin(First, Second, Third, Forth)
    return Final
    #util.raiseNotDefined()

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WumpusAlive0=logic.PropSymbolExpr('WumpusAlive',0)
    WumpusAlive1=logic.PropSymbolExpr('WumpusAlive',1)
    WumpusBorn0=logic.PropSymbolExpr('WumpusBorn',0)
    WumpusKilled0=logic.PropSymbolExpr('WumpusKilled',0)
    First= WumpusAlive1 %((WumpusAlive0 & ~WumpusKilled0) | (~WumpusAlive0 & WumpusBorn0))
    Second= ~(WumpusAlive0 & WumpusBorn0)
    Third= WumpusBorn0

    Final = logic.conjoin(First, Second, Third)

    findModel(Final)
    return Final
    

    #util.raiseNotDefined()

def modelToString(model):
    """Converts the model to a string for printing purposes. The keys of a model are 
    sorted before converting the model to a string.
    
    model: Either a boolean False or a dictionary of Expr symbols (keys) 
    and a corresponding assignment of True or False (values). This model is the output of 
    a call to logic.pycoSAT.
    """
    if model == False:
        return "False" 
    else:
        # Dictionary
        modelList = sorted(model.items(), key=lambda item: str(item[0]))
        return str(modelList)

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    to_cnf = logic.to_cnf(sentence)
    final = logic.pycoSAT(to_cnf)

    return final

def atLeastOne(literals):
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"    
    result = literals[0]
    counter=len(literals)
    for i in range(counter -1):
        result= logic.disjoin(result, literals[i+1])
    return result

def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    counter=len(literals)
    number_of_trues=0
    A=logic.Expr('A')
    for j in range(counter):
        if(literals[j]==True):
            number_of_trues+=1

    if(number_of_trues>1):
        to_return= A
    else:
        to_return=~A
    return to_return
  
def exactlyOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    
    
    
    return logic.conjoin( atLeastOne(literals), atMostOne(literals) )
                   
def bubbleSort_and_parse(arr): 
    #Sorts the array passed and makes a new one parsed (contains only the names, not the numbers)
    n = len(arr) 
    for i in range(n-1): 
        for j in range(0, n-i-1): 
            if int(logic.parseExpr(arr[j])[1]) > int(logic.parseExpr(arr[j+1])[1]) : 
                arr[j], arr[j+1] = arr[j+1], arr[j]     

    sorted_and_parsed=[]
    for i in range(n):
        sorted_and_parsed.append(logic.parseExpr(arr[i])[0])
    return sorted_and_parsed


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print(plan)
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    list_to_copy=[]
    #Miro todos los elementos del modelo y me quedo con los que sean True, tras esto me quedo solo con los que estén en actions y los copio en un array para ordenarlos.
    for i in model:
        if(model.get(i)==True):
            for j in actions:
                if(logic.parseExpr(i)[0]==j):
                    list_to_copy.append(i)
            
    #Uso bubble sort para ordenarlos ya que al ser tan pocos elementos la diferencia con otros algoritmos es minima
    final_array = bubbleSort_and_parse(list_to_copy)
    return final_array


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    print("Estoy en ",x," e ",y, " en tiempo ", t)
    ##como mucho hay 4 posibilidades: arriba abajo izquierda y derecha
    
    lista=[]
    if(walls_grid[x][y+1]==False):
        #significa que no hay una pared encima
        temp=logic.PropSymbolExpr(pacman_str, x, y+1, t-1) & logic.PropSymbolExpr("South", t-1)
        lista.append(temp)
    if(walls_grid[x][y-1]==False):
        #significa que no hay una pared debajo
        temp=logic.PropSymbolExpr(pacman_str, x, y-1, t-1) & logic.PropSymbolExpr("North", t-1)
        lista.append(temp)
    if(walls_grid[x-1][y]==False):
        #significa que no hay una pared a la iquierda
        temp=logic.PropSymbolExpr(pacman_str, x-1, y, t-1) & logic.PropSymbolExpr("East", t-1)
        lista.append(temp)
    if(walls_grid[x+1][y]==False):
        #significa que no hay una pared a la derecha
        temp=logic.PropSymbolExpr(pacman_str, x+1, y, t-1)& logic.PropSymbolExpr("West", t-1)
        lista.append(temp)

    print(walls_grid)
    final= logic.PropSymbolExpr(pacman_str, x, y, t) % (logic.disjoin(lista))
    print(final)
    return final # Replace this with your expression


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are ['North', 'East', 'South', 'West']
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    walls_list = walls.asList()
    x0, y0 = problem.getStartState()
    xg, yg = problem.getGoalState()
    
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are ['North', 'East', 'South', 'West']
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    (x0, y0), food_locations = problem.getStartState()
    food_list = food_locations.asList()    
    walls_list = walls.asList()


    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# # Abbreviations
# plp = positionLogicPlan
# flp = foodLogicPlan
# fglp = foodGhostLogicPlan



actions = ['North', 'South', 'East', 'West']
    
model = {    logic.PropSymbolExpr('South[0]'): True, 
             logic.PropSymbolExpr('East[7]'): False,
             logic.PropSymbolExpr('South[5]'): True,
             logic.PropSymbolExpr('North[6]'): True,
             logic.PropSymbolExpr('West[0]'): False, 
             logic.PropSymbolExpr('West[7]'): True,
             logic.PropSymbolExpr('South[8]'): True,
             logic.PropSymbolExpr('East[1]'): False,
             logic.PropSymbolExpr('East[10]'): True,
             logic.PropSymbolExpr('North[11]'): True,
             logic.PropSymbolExpr('South[2]'): False,
             logic.PropSymbolExpr('West[3]'): True,
             logic.PropSymbolExpr('South[4]'): True,
             logic.PropSymbolExpr('West[5]'): False,
             logic.PropSymbolExpr('East[6]'): False,
             logic.PropSymbolExpr('North[4]'): False,
             logic.PropSymbolExpr('North[8]'): False,
             logic.PropSymbolExpr('North[9]'): True,
             logic.PropSymbolExpr('East[3]'): False,
             logic.PropSymbolExpr('North[0]'): False, 
             logic.PropSymbolExpr('East[0]'): False, 
             logic.PropSymbolExpr('West[1]'): True, 
             logic.PropSymbolExpr('West[9]'): False,
             logic.PropSymbolExpr('West[10]'): False,
             logic.PropSymbolExpr('South[11]'): False,
             logic.PropSymbolExpr('South[1]'): False, 
             logic.PropSymbolExpr('North[1]'): False, 
             logic.PropSymbolExpr('North[2]'): True,
        }

plan = extractActionSequence(model, actions)
# Sometimes the logic module uses pretty deep recursion on long expressions
print("Model sentence 1:")
print(findModel(sentence1()))
print("Model sentence 2:")
print(findModel(sentence2()))
print("Model sentence 3:")
print(findModel(sentence3()))


sys.setrecursionlimit(100000)
    
