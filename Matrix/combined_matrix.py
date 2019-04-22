import time
import argparse
import numpy as np
import sys
from memory_profiler import profile, memory_usage
import psutil
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Get information about matrix')
parser.add_argument('-p','--process',help='Process', required=False, default="ir")
parser.add_argument('-s','--size',help='Size', required=False, default=int(10))
parser.add_argument('-v','--variance',help='Variance', required=False, default=int(10))
parser.add_argument('-t','--test',help='Test', required=False, default=False)
args = parser.parse_args()
isize, ivar, ipro, test = args.size, args.variance, args.process, args.test

try:
    int(isize)
    int(ivar)
except ValueError:
    print("Please enter a valid character")
    sys.exit(0)

def createMatrix(s,variance=ivar,f=0):
    if f == None:
        return np.full((int(s),int(s)),f)
    return np.array(np.random.randint(0,int(variance)+1,size=(int(s),int(s))),dtype=np.int64)

def iterative(goal,size=10):
    global matrix
    global scores_it
    global path_it

    for i in range(0,goal[0]):
            for j in range(0,goal[1]):
                if j == 0 and i == 0:
                    scores_it[0][0] = matrix[0][0]
                    path_it[0][0] = (0,0)
                    continue
                if i == 0:
                    leftCost = scores_it[0][j-1]
                    scores_it[0][j] = leftCost + matrix[0][j] + 10
                    path_it[0][j] = (0,j-1)
                    continue
                elif j == 0:
                    aboveCost = scores_it[i-1][0]
                    scores_it[i][0] = aboveCost + matrix[i][0] + 10
                    path_it[i][0] = (i-1,0)
                    continue
                else:
                    leftCost = scores_it[i-1][j] + 10
                    aboveCost = scores_it[i][j-1] + 10
                    diagonalCost = scores_it[i-1][j-1]
                
                    if min(leftCost, aboveCost, diagonalCost) == leftCost:
                        scores_it[i][j] = matrix[i][j] + leftCost
                        path_it[i][j] = (i-1,j)
                    elif min(leftCost, aboveCost, diagonalCost) == aboveCost:
                        scores_it[i][j] = matrix[i][j] + aboveCost
                        path_it[i][j] = (i,j-1)
                    else:
                        scores_it[i][j] = matrix[i][j] + diagonalCost
                        path_it[i][j] = (i-1,j-1)

def recursive(x,y,value,score):
    global matrix
    if score[y][x]!= None:
        return score[y][x]
    else:
        if x == 0 and y ==0:
            path_rec[y][x]=(0,0)
            score[y][x]=matrix[y][x]
        elif x > 0 and y>0:
            above = recursive(x,y-1,value,score)+10
            left = recursive(x-1,y,value,score)+10
            dia = recursive(x-1,y-1,value,score)
            value=min(above,left,dia)
            if value == above:
                path_rec[y][x] = (y-1,x)
            elif value == left:
                path_rec[y][x] = (y,x-1)
            else:
                path_rec[y][x] = (y-1,x-1)
            score[y][x]=value+matrix[y][x]
        elif x == 0:
            value=recursive(x,y-1,value,score)+10
            path_rec[y][x]=(y-1,x)
            score[y][x]=value+matrix[y][0]
        elif y == 0:
            value= recursive(x-1,y,value,score)+10
            path_rec[y][x]=(y,x-1)
            score[y][x]=value+matrix[0][x]
    return score[y][x]

def findPath(goal,path,score):
    global matrix
    x,y = goal[0]-1, goal[1]-1
    liste = []
    liste.append((x,y))
    while not x == 0 and not y == 0:
        x,y = liste[-1][0],liste[-1][1]
        if path[x][y] not in liste:
            liste.append(path[x][y])
    return list(reversed(liste))

if test == False:
    print("Erzeugte Matrix: \n")
    matrix = createMatrix(isize,ivar)
    print(matrix)
    if "i" in ipro:
        scores_it = createMatrix(isize,ivar,f=None)
        path_it = createMatrix(isize,ivar,f=None )
        iterative((int(isize),int(isize)),int(isize))
        print("\n Score iterativ: \n")
        print(scores_it)
        pit = findPath((int(isize),int(isize)),path_it,scores_it)
        print('\n Der minimale Aufwand beträgt {}, bei folgendem Weg: \n {} '.format(str(scores_it[int(isize)-1][int(isize)-1]),pit))
    if "r" in ipro:
        scores_rec = createMatrix(isize,ivar,f=None)
        path_rec = createMatrix(isize,ivar,f=None)
        recursive(int(isize)-1,int(isize)-1,0,scores_rec)
        print("\n Score rekursiv: \n")
        print(scores_rec)
        prec = findPath((int(isize),int(isize)),path_rec,scores_rec)
        print('\n Der minimale Aufwand beträgt {}, bei folgendem Weg: \n {} '.format(str(scores_rec[int(isize)-1][int(isize)-1]),prec))
    if "ir" in ipro or "ri" in ipro:
        if pit == prec:
            print("Pfade sind gleich")
        else:
            print("Pfade unterscheiden sich")
else:
    avg_time_it = []
    avg_time_rec = []
    avg_mem_it = []
    avg_mem_rec = []
    for i in range(10,1100,60):
        matrix = createMatrix(i,10)
        scores_it = createMatrix(i,10,f=None)
        path_it = createMatrix(i,10,f=None)
        timet1 = time.time()
        t1 = memory_usage(-1)
        iterative((int(i),int(i)),int(i))
        t2 = memory_usage(-1)
        timet2 = time.time()
        avg_mem_it.append(t2[0]-t1[0])
        avg_time_it.append(timet2-timet1)
    for j in range(10,1100,60):
        matrix = createMatrix(j,10)
        scores_rec = createMatrix(j,10,f=None)
        path_rec = createMatrix(j,10,f=None)
        timer1 = time.time()
        m1 = memory_usage(-1)[0]
        recursive(int(j)-1,int(j)-1,0,scores_rec)
        m2= memory_usage(-1)[0]
        timer2 = time.time()
        avg_mem_rec.append(m2-m1)
        avg_time_rec.append(timer2-timer1)
    x_werte=[]
    for x in range(10,1100,60):
        x_werte.append(x)
    print(x_werte, len(x_werte))
    print("Rekursiv: ",avg_time_rec)
    print("Iterativ: ",avg_time_it)
    plt.scatter(x_werte,avg_time_rec,c='r',label="rekursiv")
    plt.scatter(x_werte,avg_time_it,c='g',label="iterativ")
    plt.xlabel("Größe der Matrix")
    plt.ylabel("Dauer [s]")
    plt.title("Laufzeitanalyse rekursiver und iterativer Algorithmus")
    plt.legend(loc="upper left")
    plt.show()
    plt.scatter(x_werte,avg_mem_rec,c="r",label="rekursiv")
    plt.scatter(x_werte,avg_mem_it,c="g",label="iterativ")
    plt.xlabel("Größe der Matrix")
    plt.ylabel("Speicherverbrauch [MiB]")
    plt.title("Speicheranalyse rekursiver und iterativer Algorithmus")
    plt.legend(loc="upper left")
    plt.show()