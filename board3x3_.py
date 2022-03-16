from MonteCarloTreeSearch_ import MCTS, _Node
from EvaluationFunction_ import EvalFuncGenerator, ScalingResults, FinalEval 
from collections import namedtuple
from random import choice


_TTTB = namedtuple("Board3x3", "tup turn winner terminal")


class Board3x3(_TTTB, _Node):
    def find_children(board):
        if board.terminal:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        return {
            board.make_move(i) for i, value in enumerate(board.tup) if value is None
        }

    def find_random_child(board):
        if board.terminal:
            return None  # If the game is finished then no moves can be made
        empty_spots = [i for i, value in enumerate(board.tup) if value is None]
        return board.make_move(choice(empty_spots))

    def reward(board):
        if not board.terminal:
            raise RuntimeError(f"reward called on nonterminal board {board}")
        if board.winner is board.turn:
            if gamevar == 0:
                raise RuntimeError(f"reward called on unreachable board {board}") 
            return 1
            # It's your turn and you've already won. Should be impossible.
            
        if board.turn is (not board.winner):
            return 0  # Your opponent has just won. Bad.
        if board.winner is None:
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {board.winner}")

    def is_terminal(board):
        return board.terminal

    def make_move(board, index):
        tup = board.tup[:index] + (board.turn,) + board.tup[index + 1 :]
        turn = not board.turn
        #print("yolo:",gamevar)
        winner = _find_winner(tup,gamevar)
        is_terminal = (winner is not None) or not any(v is None for v in tup)
        return Board3x3(tup, turn, winner, is_terminal)

    def to_pretty_string(board):
        to_char = lambda v: ("X" if v is True else ("O" if v is False else " "))
        rows = [
            [to_char(board.tup[3 * row + col]) for col in range(3)] for row in range(3)
        ]
        return (
            "\n                     1 2 3\n                   "
            + "\n                   ".join(str(i + 1) + " " + " ".join(row) for i, row in enumerate(rows))
            + "\n                   "
        )

gamevar=0
def ModuleConnector(game):
    global gamevar
    gamevar=game
    
def play_game():
    global gamevar
    tree = MCTS()
    __game=input("enter game:")#0 for normal , 1 for reverse tic tac toe
    gamevar=int(__game)
    board = new_tic_tac_toe_board()
    print("gamevar",gamevar)
    print(board.to_pretty_string())
    while True:
        row_col = input("enter row,col: ")
        row, col = map(int, row_col.split(","))
        index = 3 * (row - 1) + (col - 1)
        if board.tup[index] is not None:
            raise RuntimeError("Invalid move")
        board = board.make_move(index)#index=0-8
        print(board.to_pretty_string())
        if board.terminal:
            return board.winner
            #break
        temp=converter(board[0],3,3)
        eval_func=EvalFuncGenerator(temp,'x',int(__game))
        print("Evaluation Function:",eval_func,temp)
        results=ScalingResults(temp,'x',int(__game))
        for _ in range(4000):#4000 rollouts on every MCTS cicle
            #print("---------")
           # print(board)
            tree._rollout(board,eval_func,results)
        #print("-------------------")
       # print("here we end,tree.Q:",tree.Q," tree.N:",tree.N," tree.children:",tree.children)
        board = tree.pick(board)
       # print(board)
        print(board.to_pretty_string())
        if board.terminal:
            return board.winner
            #break



def _winning_combos():
    for start in range(0, 9, 3):  # three in a row
        yield (start, start + 1, start + 2)
    for start in range(3):  # three in a column
        yield (start, start + 3, start + 6)
    yield (0, 4, 8)  # down-right diagonal
    yield (2, 4, 6)  # down-left diagonal


def _find_winner(tup,var):
    "Returns None if no winner, True if X wins, False if O wins"
    for i1, i2, i3 in _winning_combos():
        v1, v2, v3 = tup[i1], tup[i2], tup[i3]
        if False is v1 is v2 is v3:
            return True if var is 1 else False    
        if True is v1 is v2 is v3:
            return False if var is 1 else True
    return None

def converter(tup,rows,cols):
    temp=[]
    temp1=0
    temp2=cols
    for i in range(0,rows):
        temp.append([])
        for j in range(temp1,temp2):
            if tup[j]==None:
                temp[i].append('-')
            elif tup[j]==True:
                temp[i].append('x')
            else:
                temp[i].append('o')
            
        temp1=temp1+cols
        temp2=temp2+cols
    return temp

def new_tic_tac_toe_board():
    return Board3x3(tup=(None,) * 9, turn=True, winner=None, terminal=False)


if __name__ == "__main__":
    print(play_game())
   
