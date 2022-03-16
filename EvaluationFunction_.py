import copy
import random
import math



def initial(board):
    cells=[]
    cell=[]
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j]=='-':
                board[i][j]='b'
            cell=[i+1,j+1,board[i][j]]
            cells.append(cell)
    return cells

total=[]
def general(cells):
    global total
    total=cells
    
    for i in range(0,len(cells)):
        for j in range(0,3):
            temp=copy.deepcopy(cells[i])
            temp[j]='?'
            if temp not in total:
                total.append(temp)
            if temp[0]=='?' and temp[1]=='?' and temp[2]=='?':
                return 
    general(total)
           
    
def special(cells):
    global total
    constants1=['x','o','b']
    constants2=[1,2,3]
    total=cells
    for i in range(0,len(cells)):
        for j in range(0,3):
            if j==len(cells[i])-1 and cells[i][j]=='?':
                for k in constants1:
                    #cells[i][j]=k
                    temp=copy.deepcopy(cells[i])
                    temp[j]=k
                    if temp not in total:
                        total.append(temp)
            if j!=len(cells[i])-1 and cells[i][j]=='?' :
                for k in constants2:
                    #cells[i][j]=k
                    temp=copy.deepcopy(cells[i])
                    temp[j]=k
                    if temp not in total:
                        total.append(temp)
features=[]#list of feature objects

class feature:

    def __init__(self,row,column,stat):
        self.row=row
        self.column=column
        self.stat=stat
        self.totscore=0
        self.avgscore=0
        self.score=[]
        self.totalsims=0
        self.svtotscore=[]
        self.svavgscore=[]
        self.svsims=0
        self.tv=0
        self.sv=[]
        self.sv2=[]
        self.avsv=0
        self.avsv2=0
        self.stability=0
        self.stability2=0
        self.corelscore=[]
        self.corel=0
        self.feat=[self.row,self.column,self.stat]
    
    def printfeature(self):
        return [[self.row,self.column,self.stat],[self.totsims]]

def features_creation():
    global features
    global total
    general(initial([['-','-','-'],['-','-','-'],['-','-','-']]))
    special(total)
    for i in range(0,len(total)):
        features.append(feature(total[i][0],total[i][1],total[i][2]))
        
def features_update(board):
    global features
    startb=initial(board)
    constants1=['x','o','b']
    constants2=[1,2,3]
    temp0=[]
    tempscore=0
    for i in range(0,len(features)):
        for j in range(0,len(features[i].feat)):
            if features[i].row=='?':
                temp1=constants2[j]
            else:
                temp1=features[i].row
            for k in range(0,len(features[i].feat)):
                if features[i].column=='?':
                    temp2=constants2[k]
                else:
                    temp2=features[i].column
                for l in range(0,len(features[i].feat)):
                    if features[i].stat=='?':
                        temp3=constants1[l]
                    else:
                        temp3=features[i].stat
                    if [temp1,temp2,temp3] not in temp0:
                        temp0.append([temp1,temp2,temp3])
                        if [temp1,temp2,temp3] in startb:
                            features[i].totscore=features[i].totscore+1
                            tempscore=tempscore+1
                            
        temp0.clear()
        features[i].score.append(tempscore)
        tempscore=0
    
    for i in range(0,len(features)):
        features[i].totalsims=features[i].totalsims+1
     #   if features[i].tempsims!=0:
     #       features[i].totscore=features[i].totscore+1
     #   features[i].tempsims=0
            
                                     
def MovesLeft(board):
    temp=0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j]=='-':
                return True
    return False                    
            
def evaluate(b,game):
    # Checking for Rows for X or O victory.
    #print(game,type(game))
    temp=game
    for row in range(0, 3):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == 'x':
                return 1-temp
            elif b[row][0]=='o':
                return 0+temp

    # Checking for Columns for X or O victory. 
    for col in range(0, 3):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            if b[0][col]=='x':
                return 1-temp
            elif b[0][col] == 'o':
                return 0+temp

    # Checking for Diagonals for X or O victory. 
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == 'x':
            return 1-temp
        elif b[0][0] == 'o':
            return 0+temp
    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == 'x':
            return 1-temp
        elif b[0][2] == 'o':
            return 0+temp
	
    # Else if none of them have won then return 0 
    return 0.5

svhelper=[]    
def rollout(board,ftoplay,game):
    global svhelper
    
    play1='x'
    play2='o'
    numofx=0
    numofo=0
    for i in range(0,len(board)):
                numofx=numofx+board[i].count('x')
                numofo=numofo+board[i].count('o')
    if numofx>numofo:
        toplay='o'
    else:
        toplay=ftoplay
    while True:
        temp=copy.deepcopy(board)
        #print(temp)
        features_update(temp)
        p_moves=[]
        if evaluate(board,game)==1:
            svhelper.append(features[0].totalsims)
            return 1
        if evaluate(board,game)==0:
            svhelper.append(features[0].totalsims)
            return 0
        if MovesLeft(board)==False:
            svhelper.append(features[0].totalsims)
            return 0.5
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j]=='-':
                    p_moves.append([i,j])
        if toplay==play1:
            templay='x'
            toplay='o'
        else:
            templay='o'
            toplay='x'
        mychoice=random.choice(p_moves)
        board[mychoice[0]][mychoice[1]]=templay    
    
def random_game_sequence(board,ftoplay,game):
    play1='x'
    play2='o'
    numof_=0
    numofo=0
    numofx=0
    for i in range(0,len(board)):
                numof_=numof_+board[i].count('-')
                numofx=numofx+board[i].count('x')
                numofo=numofo+board[i].count('o')
    #print("kena=",numof_)
    if numofx>numofo:
        toplay='o'
    else:
        toplay=ftoplay
    if numof_>=4:
        randepth=random.randint(0,3)
    else:
        randepth=random.randint(0,numof_)
        
    while True:
        if randepth==0:
            #print("rand",randepth,board)
            return board
        if evaluate(board,game)==1:
           # print("1",board)
            return board
        if evaluate(board,game)==0:
            #print("0",board)
            return board
        if MovesLeft(board)==False:
            #print("false",board)
            return board
        p_moves=[]
        for i in range(0,len(board)):
            for j in range(0,len(board[i])):
                if board[i][j]=='-':
                    p_moves.append([i,j])
        if toplay==play1:
            templay='x'
            toplay='o'
        else:
            templay='o'
            toplay='x'
        mychoice=random.choice(p_moves)
        board[mychoice[0]][mychoice[1]]=templay
        randepth=randepth-1

def random_game_sequence2(board,ftoplay,game):
    play1='x'
    play2='o'
    numof_=0
    numofo=0
    numofx=0
    for i in range(0,len(board)):
                numof_=numof_+board[i].count('-')
                numofx=numofx+board[i].count('x')
                numofo=numofo+board[i].count('o')
    #print("kena=",numof_)
    if numofx>numofo:
        toplay='o'
    else:
        toplay=ftoplay
    if numof_==0:
        randepth=0
    else:
        randepth=random.randint(1,numof_)
    #print(randepth)
        
    while True:
        if randepth==0:
            #print("rand",randepth,board)
            return board
        if evaluate(board,game)==1:
           # print("1",board)
            return board
        if evaluate(board,game)==0:
            #print("0",board)
            return board
        if MovesLeft(board)==False:
            #print("false",board)
            return board
        p_moves=[]
        for i in range(0,len(board)):
            for j in range(0,len(board[i])):
                if board[i][j]=='-':
                    p_moves.append([i,j])
        if toplay==play1:
            templay='x'
            toplay='o'
        else:
            templay='o'
            toplay='x'
        mychoice=random.choice(p_moves)
        board[mychoice[0]][mychoice[1]]=templay
        randepth=randepth-1
        
EvaluationFunction={}

def EvalFuncGenerator(board,ftoplay,game):
    global features
    global total
    global svhelper
    global EvaluationFunction
    Evaluation_Function={}
    evalfunctiontemp={}
    evaltemp=""
    rollresults=[]
    avgrollresperseq=[]
    rolltemp=0
    tempcorel1=0
    tempcorel2=0
    tempcorel3=0
    otemp=0
    ontemp=0
    sumtemp=0
    maxtemp=0
    temper=[]
    sv_avgvalue=0
    sv_simsperseq=0
    sv_allsims=[]
    sv_totscore=0
    sval=0
    temp=copy.deepcopy(board)
    sequences=[]
    features_creation()
    #features_update(board)
    for i in range(0,100):
        sequences.append(random_game_sequence(temp,ftoplay,game))
        temp=copy.deepcopy(board)
    for i in range(0,100):
        #print(sequences[i])
        for rolls in range(0,10):
            temp2=copy.deepcopy(sequences[i])
            #print(temp2)
            rollresults.append(rollout(temp2,'x',game))
           
       
    for i in range(0,len(svhelper)):
        if i==0:
            temper.append(svhelper[i])
        else:
            temper.append(svhelper[i]-svhelper[i-1])
    svhelper=temper.copy()
    
    for i in range(0,len(features)):
        features[i].avgscore=features[i].totscore/features[i].totalsims
        for j in range(0,features[i].totalsims):
            features[i].tv=features[i].tv+(features[i].score[j]-features[i].avgscore)**2
        features[i].tv=features[i].tv/features[i].totalsims

    
    for i in range(0,len(svhelper)):
        sv_simsperseq=sv_simsperseq+svhelper[i]
        if (i+1)%10==0:
            sv_allsims.append(sv_simsperseq)
            sv_simsperseq=0
    #print("len sv_allsims:",len(sv_allsims))
    #for i in range(0,len(sv_allsims)):
       # print(sv_allsims[i])
            
        
    for i in range(0,len(features)):
        for seqsims in range(0,len(sv_allsims)):
            for sims in range(otemp,sv_allsims[seqsims]+otemp):
                #print(i)
                sv_totscore=sv_totscore+features[i].score[sims]
                #print(sims,"otemp:",otemp,"sv_allsims[seqsims]+otemp:",sv_allsims[seqsims]+otemp)
            otemp=otemp+sv_allsims[seqsims]
            features[i].svtotscore.append(sv_totscore)
            sv_avgvalue=sv_totscore/sv_allsims[seqsims]
            features[i].svavgscore.append(sv_avgvalue)
            sv_totscore=0
            sv_avgvalue=0
        otemp=0
    for i in range(0,len(features)):
        for seqsims in range(0,len(sv_allsims)):
            for sims in range(ontemp,sv_allsims[seqsims]+ontemp):
                sval=sval+(features[i].score[sims]-features[i].svavgscore[seqsims])**2
            ontemp=ontemp+sv_allsims[seqsims]
            sval=sval/sv_allsims[seqsims]
            features[i].sv.append(sval)
            sval=0
        ontemp=0
    
    for i in range(0,len(features)):
        for j in range(0,len(features[i].sv)):
            sumtemp=sumtemp+features[i].sv[j]
        features[i].avsv=sumtemp/100
        sumtemp=0
    
    
    for i in range(0,len(features)):
        if features[i].avsv!=0:
            features[i].stability=(features[i].tv)/(features[i].tv+10*features[i].avsv)
            if features[i].stability>maxtemp:
                maxtemp=features[i].stability
    for i in range(0,len(features)):
        if features[i].avsv==0:
            features[i].stability=maxtemp+0.05

    #
    #maxtemp=0#
    #for i in range(0,len(features)):#
        #if features[i].avsv2!=0:#
            #features[i].stability2=(features[i].tv)/(features[i].tv+10*features[i].avsv2)#
           # if features[i].stability2>maxtemp:#
               # maxtemp=features[i].stability2#
   # for i in range(0,len(features)):#
       # if features[i].avsv2==0:#
           # features[i].stability2=maxtemp+0.05#
            
    for i in range(0,len(rollresults)):
        rolltemp=rolltemp+rollresults[i]
        if(i+1)%10==0:
            avgrollresperseq.append(rolltemp/10)
            rolltemp=0

    otemp=0
    for i in range(0,len(features)):
        for j in range(0,1000):
                   features[i].corelscore.append(features[i].score[svhelper[j]+otemp-1])
                   otemp=otemp+svhelper[j]
        otemp=0
    otemp=0
    
    for i in range(0,len(features)):
        for j in range(0,1000):
            tempcorel1=tempcorel1+(features[i].corelscore[j]-features[i].avgscore)*(rollresults[j]-avgrollresperseq[j-otemp])
            tempcorel2=tempcorel2+(features[i].corelscore[j]-features[i].avgscore)**2
            tempcorel3=tempcorel3+(rollresults[j]-avgrollresperseq[j-otemp])**2
            otemp=otemp+1
            if (j+1)%10==0:
                otemp=otemp-1
        if tempcorel1!=0:
            features[i].corel=tempcorel1/(math.sqrt(tempcorel2*tempcorel3))
        else:
            features[i].corel=0
        tempcorel1=0
        tempcorel2=0
        tempcorel3=0
        otemp=0
            
            
    for i in range(0,len(features)):
        for j in range(0,len(features[i].feat)):
            evaltemp=evaltemp+str(features[i].feat[j])
            
        evalfunctiontemp[evaltemp]=min(features[i].stability,abs(features[i].corel))
        evaltemp=""
            
    sortedkeys=sorted(evalfunctiontemp,key=evalfunctiontemp.get,reverse=True)
    
    returntemp=[]
    for i in range(0,len(sortedkeys)):
        returntemp.append([])
    for i in range(0,len(sortedkeys)):
        for j in range(0,len(sortedkeys[i])):
            if sortedkeys[i][j]!='x' and sortedkeys[i][j]!='o' and sortedkeys[i][j]!='?' and sortedkeys[i][j]!='b':
                returntemp[i].append(int(sortedkeys[i][j]))
            else:
                returntemp[i].append(sortedkeys[i][j])
                
    temp=converter(returntemp)
    for i in range(0,30):
        for j in range(0,len(features)):
            if returntemp[i]==features[j].feat:
                Evaluation_Function[temp[i]]=round(features[j].corel*features[j].stability,4)
    average=0
    for i in range(0,len(rollresults)):
        average=average+rollresults[i]
        
    Evaluation_Function["Average_Value"]=round(average/1000,4)

    
    
    
        
    EvaluationFunction=Evaluation_Function

    features=[]
    total=[]
    svhelper=[]
    return Evaluation_Function
            
        



    

def converter(listorstr):
    temp=[]
    tempstr=""
    if type(listorstr[0])==list:
        for i in range(0,len(listorstr)):
            for j in range(0,len(listorstr[i])):
                tempstr=tempstr+str(listorstr[i][j])
            temp.append(tempstr)
            tempstr=""
    else:
        for i in range(0,len(listorstr)):
            temp.append([])
            for j in range(0,len(listorstr[i])):
                if listorstr[i][j]!='x' and listorstr[i][j]!='o' and listorstr[i][j]!='b' and listorstr[i][j]!='?':
                    temp[i].append(int(listorstr[i][j]))
                else:
                    temp[i].append(listorstr[i][j])
    return temp
            

def node(board,eval_function):
    global features
    features=[]
    temp=[]
    result=0
    for i in eval_function.keys():
        if i!="Average_Value":
            temp.append(i)
    temp=converter(temp)
    for i in range(0,len(temp)):
        #print(temp[i])
        features.append(feature(temp[i][0],temp[i][1],temp[i][2]))
    
    #print("------------------------------------------------------------")
    features_update(board)
    #for i in range(0,len(features)):
        #print(features[i].feat,features[i].score[0])
    temp=converter(temp)
    for i in range(0,30):
        result=result+features[i].score[0]*eval_function[temp[i]]
    features=[]
    #print(result)
    return result

def ScalingResults(board,ftoplay,game):
    global EvaluationFunction
    temp2=copy.deepcopy(board)
    avg=0
    res=[]
    for i in range(0,2000):
        temp=copy.deepcopy(random_game_sequence2(temp2,ftoplay,game))
        #print(temp)
        res.append(node(temp,EvaluationFunction))
        #print(i)
        temp2=copy.deepcopy(board)
    for i in range(0,2000):
        avg=avg+res[i]
    print(len(res))
    print("min:",round(min(res),2),"max:",round(max(res),2),"avg:",round(avg/2000,2))
    return [min(res),avg/2000,max(res)]

def FinalEval(board,results,evalf):
    
    result=node(board,evalf)
    if result==0 or result<results[0] or result>results[2]:
        return evalf["Average_Value"]
    if results[0]*results[1]>0:
        temp1=round((results[0]+results[1])/2,2)
    else:
        temp1=round((abs(results[0])+abs(results[1]))/2+results[0],2)
    if results[1]*results[2]>0:
        temp2=round((results[1]+results[2])/2,2)
    else:
        temp2=round(results[2]-(abs(results[1])+abs(results[2]))/2,2)

    #print("result:",result,"---",temp1,temp2)

    if result<=temp1:
        return 0
    elif result>=temp2:
        return 1
    else:
        return 0.5

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
    
    
    
    
    
    


                

        
        


