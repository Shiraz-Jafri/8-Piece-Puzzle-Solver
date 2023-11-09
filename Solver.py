#!/usr/bin/python3

import State
import Board
import heapq
STOP = -1
CONTINUE = 0

# THE FOLLOWING PROGRAM IS AN AI THAT SOLVES AN 8-PIECE PUZZLE BY APPLYING NUMEROUS ALGORITHMS (BFS, UNIFORM COST SEARCH, MANHATTAN DISTANCE HEURISTIC).

# expand_fringe function adds the possible states that we can get to
# from the current state to the end of the fringe.

def expand_fringe(current_state, fringe):
    Board = current_state.board
    if Board.slide_blank((-1, 0)) != None:
        downBoard = Board.slide_blank((-1, 0))
        downState = State.State(downBoard, current_state, current_state.depth + 1, 0)
        fringe.append(downState)
    if Board.slide_blank((1, 0)) != None:
        upBoard = Board.slide_blank((1, 0))
        upState = State.State(upBoard, current_state, current_state.depth + 1, 0)
        fringe.append(upState)
    if Board.slide_blank((0, 1)) != None:
        leftBoard = Board.slide_blank((0, 1))
        leftState = State.State(leftBoard, current_state, current_state.depth + 1, 0)
        fringe.append(leftState)
    if Board.slide_blank((0, -1)) != None:
        rightBoard = Board.slide_blank((0, - 1))
        rightState = State.State(rightBoard, current_state, current_state.depth + 1, 0)
        fringe.append(rightState)


        
# breadth_first_search function performs BFS algorithm on the current state of the board
# after the algorithm, the new state gets added to the fringe.

def breadth_first_search(fringe, max_depth, goal_board):
    if len(fringe) == 0 :
        return STOP
    state = fringe.pop(0)
    if state.depth > max_depth :
        return CONTINUE
    if state.board == goal_board:
        return state
    expand_fringe(state, fringe)
    return CONTINUE

# uninformed_solver will call breadth_first_search in a loop until it finds a solution

def uninformed_solver(start_board, max_depth, goal_board):
    fringe = [State.State(start_board, None, 0, 0)]
    found = CONTINUE
    while found == CONTINUE:
        found = breadth_first_search(fringe, max_depth, goal_board)
    if isinstance(found, State.State):
        # Found goal!
        return found
    # Max depth reached...
    return None

# ucs_f_function applies uniform cost search on given state by taking a board and depth and returning the f-value
# (priority) that board should have in a uniform-cost search scenario.
def ucs_f_function(board, current_depth):
    return current_depth
# a_star_f_function_factory is a function that takes a
# heuristic function and a goal board, returns a f-value FUNCTION (like ucs_f_function) 
# that evaluates boards and depths as in the A* algorithm.

def a_star_f_function_factory(heuristic, goal_board):
    return lambda board, depth : heuristic(board, goal_board) + depth

# Example Heuristic function
def manhattan_distance(current_board, goal_board):
    total = 0
    goal_matrix = goal_board.matrix
    for goal_r in range(len(goal_board.matrix)):
        for goal_c in range(len(goal_board.matrix[0])):
            val = goal_matrix[goal_r][goal_c]
            if val == 0:
                continue
            print(val)
            current_r, current_c = current_board.find_element(val)
            total += abs(goal_r - current_r) + abs(goal_c - current_c)
    return total

# informed_expansion is a function that applies the given f_function on the current_state of the game
# and updates the fringe with the new state.
def informed_expansion(current_state, fringe, f_function):
    Board = current_state.board
    heapq.heapify(fringe)
    if Board.slide_blank((-1, 0)) != None:
        downBoard = Board.slide_blank((-1, 0))
        downState = State.State(downBoard, current_state, current_state.depth + 1, 0)
        downState.fvalue = f_function(downBoard, current_state.depth + 1)
        heapq.heappush(fringe, downState)
    if Board.slide_blank((1, 0)) != None:
        upBoard = Board.slide_blank((1, 0))
        upState = State.State(upBoard, current_state, current_state.depth + 1, 0)
        upState.fvalue = f_function(upBoard, current_state.depth + 1)
        heapq.heappush(fringe, upState)
    if Board.slide_blank((0, 1)) != None:
        leftBoard = Board.slide_blank((0, 1))
        leftState = State.State(leftBoard, current_state, current_state.depth + 1, 0)
        leftState.fvalue = f_function(leftBoard, current_state.depth + 1)
        heapq.heappush(fringe, leftState)
    if Board.slide_blank((0, -1)) != None:
        rightBoard = Board.slide_blank((0, - 1))
        rightState = State.State(rightBoard, current_state, current_state.depth + 1, 0)
        rightState.fvalue = f_function(rightBoard, current_state.depth + 1)
        heapq.heappush(fringe, rightState)
        

# informed_search function will apply Informed search on the fringe through
# implementation of single iteration of the UCS Algorithm by considering the top priority 
# state from the given fringe.

def informed_search(fringe, goal_board, f_function, explored):
    if (len(fringe) == 0):
        return STOP
    else:
        top_state = heapq.heappop(fringe)
        top_state.fvalue = f_function(top_state.board, top_state.depth)
        if top_state.board in explored.values():
            value = {i for i in explored if dic[i]==top_state.board}
            if value.get("fvalue") < top_state.fvalue:
                top_state.fvalue = value.get("fvalue")
                explored.update()
            else:
                return CONTINUE
        if top_state.board == goal_board:
            newValue = {"fvalue" : 0}
            explored.update(newValue)
            return top_state
        explored[top_state.board] = top_state.fvalue
        informed_expansion(top_state, fringe, f_function)
        return CONTINUE

# informed_solver is a function that runs in a loop while applying informed_search function
# until it finds a solution.

def informed_solver(start_board, goal_board, f_function):
   
    fringe = [State.State(start_board, None, 0, f_function(start_board, 0))]
    explored = {}
    found = CONTINUE
    while found == CONTINUE:
        found = informed_search(fringe, goal_board, f_function, explored)
    if isinstance(found, State.State):
        return found
    return None
def ucs_solver(start_board, goal_board):
    return informed_solver(start_board, goal_board, ucs_f_function)
def a_star_solver(start_board, goal_board, heuristic):
    f_function = a_star_f_function_factory(heuristic, goal_board)
    return informed_solver(start_board, goal_board, f_function)

def main():
    board = Board.Board([[1, 0, 3],
                   [4, 2, 6],
                   [7, 5, 8]])
    goal_board = Board.Board([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 0]])
    print(ucs_solver(board, goal_board))



main()
