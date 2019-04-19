import time
import argparse
import numpy as np
import sys
import resource

parser = argparse.ArgumentParser(description='Get information about matrix')
parser.add_argument('-p','--process',help='Process', required=False, default="ir")
parser.add_argument('-s','--size',help='Size', required=False, default=int(10))
parser.add_argument('-v','--variance',help='Variance', required=False, default=10)
args = parser.parse_args()
isize, ivar, ipro = args.size, args.variance, args.process

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
           score[y][x]=matrix[y][x]
        elif x > 0 and y>0:
            value=min(recursive(x,y-1,value,score)+10,recursive(x-1,y,value,score)+10,recursive(x-1,y-1,value,score))
            score[y][x]=value+matrix[y][x]
        elif x == 0:
            value=recursive(x,y-1,value,score)+10
            score[y][x]=value+matrix[y][0]
        elif y == 0:
            value= recursive(x-1,y,value,score)+10
            score[y][x]=value+matrix[0][x]
    return score[y][x]

def findPath(goal):
    global path_it
    global matrix
    x,y = goal[0]-1, goal[1]-1
    liste = []
    liste.append((x,y))
    while not x == 0 and not y == 0:
        x,y = liste[-1][0],liste[-1][1]
        if path_it[x][y] not in liste:
            liste.append(path_it[x][y])
    print('\n Der minimale Aufwand beträgt {}, bei folgendem Weg: '.format(str(scores_it[goal[0]-1][goal[1]-1])))
    for element in list(reversed(liste)):
        print(element)

print("Erzeugte Matrix: \n")
matrix = createMatrix(isize,ivar)
print(matrix)
if "i" in ipro:
    scores_it = createMatrix(isize,ivar,f=None)
    path_it = createMatrix(isize,ivar,f=None )
    iterative((int(isize),int(isize)),int(isize))
    print("\n Score iterativ: \n")
    print(scores_it)
    findPath((int(isize),int(isize)))

if "r" in ipro:
    scores_rec = createMatrix(isize,ivar,f=None)
    path_rec = createMatrix(isize,ivar,f=None)
    recursive(int(isize)-1,int(isize)-1,0,scores_rec)
    print("\n Score rekursiv: \n")
    print(scores_rec)


    