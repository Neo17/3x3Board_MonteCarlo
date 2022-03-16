from board3x3_ import play_game, new_tic_tac_toe_board, converter,  ModuleConnector
from MonteCarloTreeSearch_ import MCTS, _Node
from EvaluationFunction_ import EvalFuncGenerator, ScalingResults, FinalEval
import random

#Testing module---->MCTS will play 100 games(50 in tic-tac-toe and 50 in misere tic-tac-toe against a player who plays random moves
# in the end results will be presented.This testing will take a while ...

def testing(sims,game):
    tree = MCTS()
    board = new_tic_tac_toe_board()
    ModuleConnector(game)
    while True:
        p_moves=[]
        for i in range(0,len(board[0])):
            if board[0][i]==None:
                p_moves.append(i)
        index=random.choice(p_moves)
        board = board.make_move(index)#index=0-8 
        print(board.to_pretty_string())
        if board.terminal:
            return board.winner
            #break
        temp=converter(board[0],3,3)
        eval_func=EvalFuncGenerator(temp,'x',game)
        print("here:",eval_func,temp)
        results=ScalingResults(temp,'x',game)
        for _ in range(sims):#x rollouts on every MCTS cicle
            #print("---------")
           # print(board)
            tree._rollout(board,eval_func,results)
        #print("-------------------")
        board = tree.pick(board)
       # print(board)
        print(board.to_pretty_string())
        if board.terminal:
            return board.winner
            #break

if __name__ == "__main__":
    tempx0=0
    tempo0=0
    tempd0=0
    counter=50
    while counter!=0:
        temp=testing(1000,0)
        if temp==True:
            tempx0+=1
        elif temp==False:
            tempo0+=1
        else:
            tempd0+=1
        counter-=1
    
    
    tempx=0
    tempo=0
    tempd=0
    counter=50
    while counter!=0:
        temp=testing(1000,1)
        if temp==True:
            tempx+=1
        elif temp==False:
            tempo+=1
        else:
            tempd+=1
        counter-=1
    print("------------------------------------------------------------------------------")
    print("After 50 games using 1000 sims per MCTS circle in the game of Tic-Tac-Toe")
    print("Random player wins:",tempx0,"AI MCTS(with Eval.Function) wins:",tempo0," Draws:",tempd0)
    print("------------------------------------------------------------------------------")
    print("After 50 games using 1000 sims per MCTS circle in the game of Misere Tic-Tac-Toe")
    print("Random player wins:",tempx,"AI MCTS(with Eval.Function) wins:",tempo," Draws:",tempd)        
        


