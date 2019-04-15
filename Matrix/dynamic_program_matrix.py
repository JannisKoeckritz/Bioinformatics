import random
import time
import argparse
import numpy as np

"""
The following block allows to pass the arguments 'size' (-s/--size) and 'variance' (-v/--variance) 
through the command-line to the script. They are optional.
Usage: 'python3 dynamic_program_matrix.py -s 10 -v 20' for 10x10 matrix with values from 0 to 20.
"""
parser = argparse.ArgumentParser(description='Get information about matrix')
parser.add_argument('-s','--size',help='Size', required=False)
parser.add_argument('-v','--variance',help='Variance', required=False)
args = parser.parse_args()
isize, ivar = args.size, args.variance
if isize == None:
    isize = 10
if ivar == None:
    ivar = 10

try:
    int(isize)
    int(ivar)
except ValueError:
    print("Please enter a valid number")

#Function creates random matrix with optional parameters (size and variance) 
def createMatrix(s=10,varianz=10):
    return np.array(np.random.randint(0,varianz+1,size=(int(s),int(s))))

#Function creates scoring matrix with the same size as matrix created above. All cells get th same value ("*")
def createHomoMatrix(s=10,value=99999999):
    return [[value for x in range(0,s)] for y in range(0,s)]

#Core function. Works through recursion.
def calcValue(x,y,value):
    if x == 0 and y ==0: #
        scores[y][x]=maze[y][x]
        value=0
    else:
        if y >0 and x >0:
            if scores[y][x]=="*":
                value=min(calcValue(x,y-1,value)[2],calcValue(x-1,y,value)[2],calcValue(x-1,y-1,value)[2])
                scores[y][x]=value+maze[y][x]
            else: value=scores[y][x]
        elif x == 0:
            if scores[y][0]=="*":
                value=calcValue(x,y-1,value)[2]
                scores[y][0]=value+maze[y][0]
            else: value=scores[y][0]
        elif y == 0:
            if scores[0][x]=="*":
                value= calcValue(x-1,y,value)[2]
                scores[0][x]=value+maze[0][x]
            else: value=scores[0][x]
    posValue=value+maze[y][x]
    return [x,y,posValue]

maze=createMatrix(int(isize),int(ivar))
print(maze)
scores=createHomoMatrix(int(isize),"*")
time1=time.time()
calcValue(len(maze)-1,len(maze)-1,0)
time2=time.time()

for zeile in scores:
    print(zeile)
print("Duration: ",time2-time1)