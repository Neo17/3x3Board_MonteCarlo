import math
import random
from EvaluationFunction_ import FinalEval
from collections import defaultdict



class _Node():#The basic node .You can implement these methods to any game 
    
    def find_random_child(self):
        return None
    
    def find_children(self):
        return set()

    def is_terminal(self):
        return True

    def reward(self):
        return 0

def converter2(tup,rows,cols):
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

def list_reverse(l):
    temp=[]
    for i in range(0,len(l)):
        temp.append(l[len(l)-1-i])
    return temp   


class MCTS:#the whole idea of this Monte Carlo Tree search is based on a dictionary implementation.The idea of a list has been also tried with no success

    def __init__(self, exploration_weight=1):
        self.Value = defaultdict(int)  # total reward of each node
        self.Visits = defaultdict(int)  # total visit count for each node
        self.children = dict()  # Another dictionary .keys are the nodes.Values of each key are the node's children.
        self.exploration_weight = exploration_weight

    def pick(self, node):#pick the best available move based on average reward
        temp=0
        #print(node)
        #print("-----------------")
        #print(self.children)
        def score(n):
            if self.Visits[n] == 0:
                return -1000 #to not be able to pick such a node.In other words this node hasnt been yet explored  
            return self.Value[n] / self.Visits[n]  # average reward

        if node not in self.children:#searching on keys
            return node.find_random_child()
        for i in self.children[node]:
            #print(i,score(i))
            if score(i)>temp:
                temp=score(i)
                temp2=i
        #print(temp2)
        return temp2

    def _uct_select(self, node):
        temp=-10000
        log_N_temper = math.log(self.Visits[node])

        def uct(n):#This the ucb method of the monte carlo explained on the paper.The best way to balance exploration and exploitation
            exploitation=self.Value[n]/self.Visits[n]
            exploration=self.exploration_weight * math.sqrt(log_N_temper / self.Visits[n])
            UCB=exploitation+exploration
            return UCB
        
        for i in self.children[node]:
            if uct(i)>temp:
                temp=uct(i)
                temp2=i
        return temp2    

    def _select(self, node):
        path = []
        #print(node)
        #print("----------------")
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                #print("path1",path)
                return path
            temp1=self.children[node]
            temp2=self.children.keys()
            temp3=temp1-temp2
            if temp3:
                new = temp3.pop()
                path.append(new)
                #print("path2",path)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        #update
        if node in self.children:
            return  # already has been expanded
        self.children[node] = node.find_children()

    def _simulate(self, node, evalfunction, results):
        invert_reward = True #Based on the fact that the player who is ready to make a move can not lose unless it's a misere game
        #print(node,node.is_terminal())
        #print(node,node[0],type(node[0]))
        if (random.randint(0,100))<10:#There is 10% chance we stop the rollout and use our evaluation function
            if node.is_terminal():
                #print(node)
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            temp=converter2(node[0],3,3)
            #print(temp)
            reward=FinalEval(temp,results,evalfunction)
            #print("bingo",reward)
            return reward # 1 for win 0.5 for a draw , 0 for a loss
        
        while True:
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            
            node = node.find_random_child()
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        #print(path,type(path),reward)
        temp1=list_reverse(path)
        for n in temp1:
            self.Visits[n] = self.Visits[n]+1
            self.Value[n] = self.Value[n]+reward
            reward = 1 - reward  

    def _rollout(self, node, evalfunction, results):
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf, evalfunction, results)#reward = 1 or 0.5 or 0
        #print(reward)
        self._backpropagate(path, reward)




