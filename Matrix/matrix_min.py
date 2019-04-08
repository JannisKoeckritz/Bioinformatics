# define the input matrix in the following format
# input = [   [3,7,1,5],
#             [6,9,2,10],
#             [11,5,37,3],
#             [2,3,1,0] ]

import numpy as np

size = int(input("Welche Größe soll die Matrix besitzen?"))

input = np.random.randint(0,10,size=(size,size))

# method that gets the matrix and a cell coordinate and 
# returns the minimal cost with the corresponding path 
def find_path(matrix, goal):
    cost_matrix = [[0 for x in range(goal[0])] for y in range(goal[1])]
    path = [[0 for x in range(goal[0])] for y in range(goal[1])]
    cost_matrix[0][0] = matrix[0][0]
    path[0][0] = (0,0)

    try:
        # getting minimal cost for all cells
        for i in range(0,goal[0]):
            for j in range(0,goal[1]):
                if j == 0 and i == 0:
                    continue
                if i == 0:
                    leftCost = cost_matrix[0][j-1]
                    cost_matrix[0][j] = leftCost + matrix[0][j]  + 10
                    path[0][j] = (0,j-1)
                    continue
                elif j == 0:
                    aboveCost = cost_matrix[i-1][0]
                    cost_matrix[i][0] = aboveCost + matrix[i][0]  + 10
                    path[i][0] = (i-1,0)
                    continue
                else:
                    leftCost = cost_matrix[i-1][j] + 10
                    aboveCost = cost_matrix[i][j-1] + 10
                    diagonalCost = cost_matrix[i-1][j-1]
                
                    if min(leftCost, aboveCost, diagonalCost) == leftCost:
                        cost_matrix[i][j] = matrix[i][j] + leftCost
                        path[i][j] = (i-1,j)
                    elif min(leftCost, aboveCost, diagonalCost) == aboveCost:
                        cost_matrix[i][j] = matrix[i][j] + aboveCost
                        path[i][j] = (i,j-1)
                    else:
                        cost_matrix[i][j] = matrix[i][j] + diagonalCost
                        path[i][j] = (i-1,j-1)

    #getting the shortest path from the path matrix
        x = goal[0]-1
        y = goal[1]-1
        liste = []
        liste.append((x,y))
        while not x == 0 and not y == 0:
            x = liste[-1][0]
            y = liste[-1][1]
            if path[x][y] not in liste:
                liste.append(path[x][y])
        print('Der minimale Aufwand beträgt {}, bei folgendem Weg: '.format(str(cost_matrix[goal[0]-1][goal[1]-1])))
        for element in list(reversed(liste)):
            print(element)
    except IndexError:
        print("Die angegebene Koordinate liegt außerhalb der Matrix.")
    
    '''
    for getting the minimal cost_matrix and 
    the path_matrix printed,comment the code below out
    '''
    # for row in cost_matrix:
    #     print(row)
    # for row in path:
    #     print(row)
find_path(input,(size,size)) # method gets matrix and goal
    