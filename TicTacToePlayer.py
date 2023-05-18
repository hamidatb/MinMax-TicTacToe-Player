"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    amount_of_X = 0
    amount_of_O = 0

    #3 rows
    for i in range(3): 
        #3 columns
        for j in range(3):
            if board[i][j] == 'X':
                amount_of_X += 1
            if board[i][j] == 'O':
                amount_of_O += 1

    if amount_of_X > amount_of_O:
        return 'O'
    elif amount_of_O > amount_of_X:
        return 'X'
    elif amount_of_O == amount_of_X:
        return 'X'
            


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    options = []

    for i in range(3): 
        for j in range(3):
            if board [i][j] == EMPTY:
                options.append((i,j))
            
    print(options)
    return options
    # This should output a list of sorts
                



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action in actions(board):
        i,j = action
        new_board = [row.copy() for row in board]
        new_board[i][j] = player(new_board)
        return new_board

    else:
        raise ValueError("Invalid action")
    



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count('X') == 3:
            return 'X'
        elif row.count('O') == 3:
            return 'O'

    # Check columns
    for j in range(3):
        column = [board[i][j] for i in range(3)]
        if column.count('X') == 3:
            return 'X'
        elif column.count('O') == 3:
            return 'O'

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        winner =  board[0][0]
        if board[0][0] == 'X':
            return 'X'
        if board[0][0] == 'O':
            return 'O'
        
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        winner =  board[0][2]
        if board[0][2] == 'X':
            return 'X'
        if board[0][2] == 'O':
            return 'O'
    

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board) == None:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    alpha = -math.inf
    beta = math.inf

    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action), alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action), alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v

    best_action = None
    if player(board) == X:
        best_score = -math.inf
        for action in actions(board):
            min_val = min_value(result(board, action), alpha, beta)
            if min_val > best_score:
                best_score = min_val
                best_action = action
                alpha = max(alpha, best_score)
                    # alpha = the lower bound on the possible scores that the maximizer 
                    # (the player who wants to maximize the score) can achieve.

    else:
        best_score = math.inf
        for action in actions(board):
            max_val = max_value(result(board, action), alpha, beta)
            if max_val < best_score:
                best_score = max_val
                best_action = action
                beta = min(beta, best_score)

    return best_action
