import random
import time
import argparse
import numpy as np

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

def createMatrix(x=10,varianz=10):
    return np.array(np.random.randint(0,varianz+1,size=(int(x),int(x))))

def createHomoMatrix(wert=99999999,x=10):
    return [[wert for x in range(0,x)] for y in range(0,x)]

def beamter(x,y,wert):
    if x == 0 and y ==0:
        werte[y][x]=labyrinth[y][x]
        wert=0
    else:
        if y >0 and x >0:
            if werte[y][x]=="*":
                wert=min(beamter(x,y-1,wert)[2],beamter(x-1,y,wert)[2],beamter(x-1,y-1,wert)[2])
                werte[y][x]=wert+labyrinth[y][x]
            else: wert=werte[y][x]
        elif x == 0:
            if werte[y][0]=="*":
                wert=beamter(x,y-1,wert)[2]
                werte[y][0]=wert+labyrinth[y][0]
            else: wert=werte[y][0]
        elif y == 0:
            if werte[0][x]=="*":
                wert= beamter(x-1,y,wert)[2]
                werte[0][x]=wert+labyrinth[0][x]
            else: wert=werte[0][x]
    posWert=wert+labyrinth[y][x]
    return [x,y,posWert]

labyrinth=createMatrix(int(isize),int(ivar))
print(labyrinth)
werte=createHomoMatrix("*",int(isize))
time1=time.time()
beamter(len(labyrinth)-1,len(labyrinth)-1,0)
time2=time.time()

# find_path(werte)
for zeile in werte:
    print(zeile)
print("Dauer: ",time2-time1)