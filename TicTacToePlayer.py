import math

# Constants to represent players and empty cells
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns the starting state of the board.
    The board is a 3x3 grid with all cells initially empty.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns the player who has the next turn on a given board.
    Counts the number of X's and O's to determine the current player.
    """
    amount_of_X = sum(row.count(X) for row in board)
    amount_of_O = sum(row.count(O) for row in board)
    return X if amount_of_X <= amount_of_O else O

def actions(board):
    """
    Returns a set of all possible actions (i, j) available on the board.
    Each action is represented as a tuple (i, j) where 'i' is the row and 'j' is the column.
    """
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY]

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Raises an exception if the action is invalid.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game if there is one.
    Checks rows, columns, and diagonals for a winning line.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if the game is over (either there is a winner or the board is full), False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board using the minimax algorithm with alpha-beta pruning.
    """

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

    current_player = player(board)
    best_action = None
    if current_player == X:
        best_score = -math.inf
        for action in actions(board):
            score = min_value(result(board, action), -math.inf, math.inf)
            if score > best_score:
                best_score = score
                best_action = action
    else:
        best_score = math.inf
        for action in actions(board):
            score = max_value(result(board, action), -math.inf, math.inf)
            if score < best_score:
                best_score = score
                best_action = action

    return best_action

def print_board(board):
    """
    Prints the current state of the board in a readable format.
    """
    for row in board:
        print(' | '.join([cell if cell is not None else ' ' for cell in row]))
        print('-' * 5)

def play_game():
    """
    Facilitates playing a game of Tic Tac Toe between a human and the AI.
    The human player is always 'O' and the AI is always 'X'.
    """
    board = initial_state()
    while not terminal(board):
        print_board(board)
        if player(board) == O:
            row = int(input("Enter the row (0, 1, 2): "))
            col = int(input("Enter the column (0, 1, 2): "))
            if (row, col) in actions(board):
                board = result(board, (row, col))
            else:
                print("Invalid move. Try again.")
        else:
            print("AI is making a move...")
            board = result(board, minimax(board))

    print_board(board)
    if winner(board):
        print(f"Winner: {winner(board)}")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
