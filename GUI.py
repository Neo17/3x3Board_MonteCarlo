import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
from board3x3_ import play_game, new_tic_tac_toe_board, converter,  ModuleConnector, Board3x3
from MonteCarloTreeSearch_ import MCTS, _Node
from EvaluationFunction_ import EvalFuncGenerator, ScalingResults, FinalEval


#create the Tkinter window
window = Tk()

# define the size of the window in width and height using the 'geometry' method
window.geometry("600x500")

window.title("Tic-Tac-Toe Variants")


   
def config(button):
    button.config(text="X")
def click(button,number):
    global flag
    global tree
    global board
    global game
    button.config(text="X")
    input_text.set("GGP TO PLAY.Select GGP button and wait")
    
    if flag:
        board = board.make_move(number)
        if board.terminal:
            if board.winner:
                input_text.set("HUMAN WINS")
            elif board.winner==False:
                input_text.set("GGP WINS")
            else:
                input_text.set("DRAW")
            return 
        
        
def GGPFunc():
    global flag
    global tree
    global board
    global game
    if game=="Tic-Tac-Toe":
        tempg=0
    else:
        tempg=1
    temp=converter(board[0],3,3)
    eval_func=EvalFuncGenerator(temp,'x',tempg)
    print("Evaluation Function:",eval_func,temp)
    results=ScalingResults(temp,'x',tempg)
    temp1=board[0]
    for _ in range(int(sims)):
        tree._rollout(board,eval_func,results)
    board = tree.pick(board)
    temp2=board[0]
    for i in range(0,len(board[0])):
        if temp1[i]!=temp2[i]:
            buttons[i].config(text="O")
            
    if board.terminal:
            if board.winner:
                input_text.set("HUMAN WINS")
            elif board.winner==False:
                input_text.set("GGP WINS")
            else:
                input_text.set("DRAW")
            return 
    input_text.set("HUMAN TO PLAY.Select your move")    
            
    

def startFunc(game1):
    temp=1
    if game1=="Tic-Tac-Toe":
        temp=0
    #print(temp)
    ModuleConnector(temp)
    input_text.set("HUMAN TO PLAY.Select your move")
    
def callbackFunc(event):
    global game
    game=event.widget.get()
    #print(game,type(game))
def callbackFunc2(event2):
    global sims
    sims=event2.widget.get()
    #print("sims:",sims,type(sims))

def ButtonClear():
    global tree
    global board
    for i in range(0,len(buttons)):
        buttons[i].config(text="")
    tree = MCTS()
    board = new_tic_tac_toe_board()
    input_text.set("Select game,number of sims and press Start")
    

tree = MCTS()
board = new_tic_tac_toe_board()

flag=True
game=""
sims=0
# In order to get the instance of the input field 'StringVar()' is used
input_text = StringVar()




# The first thing is to create a frame for the input field
input_frame = Frame(window, width = 312, height = 50, bd = 0, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
input_frame.pack(side = TOP)



input_field = Entry(input_frame, font = ('arial', 18, 'bold'), textvariable = input_text, width = 50, bg = "#eee", bd = 0, justify = CENTER)
input_field.grid(row = 0, column = 0)
input_field.pack(ipady = 10) # 'ipady' is an internal padding to increase the height of input field
input_text.set("Select game,number of sims and press Start")

# Once you have the input field defined then you need a separate frame which will incorporate all the buttons inside it below the 'input field'
btns_frame = Frame(window, width = 312, height = 272.5, bg = "grey")
btns_frame.pack()


buttons=[]

zero = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black",width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(zero,0))
zero.grid(row = 1, column = 0, padx = 1, pady = 1)
buttons.append(zero)
one = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda : click(one,1))
one.grid(row = 1, column = 1, padx = 1, pady = 1)
buttons.append(one)
two = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(two,2))
two.grid(row = 1, column = 2, padx = 1, pady = 1)
buttons.append(two)


three = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(three,3))
three.grid(row = 2, column = 0, padx = 1, pady = 1)
buttons.append(three)
four = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(four,4))
four.grid(row = 2, column = 1, padx = 1, pady = 1)
buttons.append(four)
five = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width =6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(five,5))
five.grid(row = 2, column = 2, padx = 1, pady = 1)
buttons.append(five)


six = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(six,6))
six.grid(row = 3, column = 0, padx = 1, pady = 1)
buttons.append(six)
seven = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(seven,7))
seven.grid(row = 3, column = 1, padx = 1, pady = 1)
buttons.append(seven)
eight = Button(btns_frame, text = "",font="Verdana 18 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: click(eight,8))
eight.grid(row = 3, column = 2, padx = 1, pady = 1)
buttons.append(eight)

labelgame=Label(btns_frame, text = "Select Game,Sims :",  font = ("Times New Roman", 12))
labelgame.grid(row=6,column=0, padx = 1, pady = 3)
n = tk.StringVar()
gamechosen=ttk.Combobox(btns_frame, width = 14, textvariable = n)
gamechosen['values'] =('Tic-Tac-Toe',
                       'Misere Tic-Tac-Toe')
gamechosen.grid(row=6,column=1)
n2=tk.StringVar()
simschosen=ttk.Combobox(btns_frame, width = 14, textvariable = n2)
simschosen['values'] =('100','500',
                       '1000','1500','2000','2500','3000','3500','4000')
simschosen.grid(row=6,column=2)


start = Button(btns_frame, text = "START",font="Verdana 15 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: startFunc(game))
start.grid(row = 7, column = 1, padx = 1, pady = 1)

GGP = Button(btns_frame, text = "GGP",font="Verdana 15 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: GGPFunc())
GGP.grid(row = 7, column = 2, padx = 1, pady = 1)

CLEAR = Button(btns_frame, text = "CLEAR",font="Verdana 15 bold", fg = "black", width = 6, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: ButtonClear())
CLEAR.grid(row = 7, column = 0, padx = 1, pady = 1)

gamechosen.bind("<<ComboboxSelected>>", callbackFunc)
simschosen.bind("<<ComboboxSelected>>", callbackFunc2)
#gamechosen.current()


window.mainloop()

















