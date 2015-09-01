import sys, random,  time
from PPDrawer import *
color=RandomColor()
block_size=10
x=input("Input x grid size: ")
y=input("Input y grid size: ")
dimension=(int(x),int(y))
grid_dims = (int(dimension[0]/block_size) , int(dimension[1]/block_size))
cell_array = [[0 for x in range(grid_dims[0])] for x in range(grid_dims[1])]
new_cell_array=[[0 for x in range(grid_dims[0])] for x in range(grid_dims[1])]
cell_array[10][5]=1
cell_array[10][6]=1
cell_array[10][9]=1
cell_array[10][10]=1
cell_array[10][11]=1

cell_array[9][8]=1
cell_array[8][6]=1


drawer=PDrawer(dimension[0],dimension[1])
time.sleep(.1)

def check_adjacent_new(x,y):
    sum=0
    for i in [(x-1)%grid_dims[0],x,(x+1)%grid_dims[0]]:
        for j in [(y-1)%grid_dims[1],y,(y+1)%grid_dims[1]]:
            if (i,j)!=(x,y):
                sum+=cell_array[j][i]
    return sum
              


def iterate():
    global cell_array
    global new_cell_array
     
    for i in range(grid_dims[1]):
        for j in range(grid_dims[0]):
            new_cell_array[i][j]=0
            adjacent= check_adjacent_new(j,i)
            if not cell_array[i][j] and adjacent== 3:
                new_cell_array[i][j]=1
            elif cell_array[i][j] and (adjacent==2 or adjacent==3):
               new_cell_array[i][j]=1
    temp = cell_array
    cell_array=new_cell_array
    new_cell_array=temp
    

def print_grid(drawer):

    drawer.Clear()
    
    for i in range(grid_dims[1]):
        for j in range(grid_dims[0]):
            if cell_array[i][j]==1:
                drawer.AddEllipse(block_size*j,block_size*i,block_size,block_size,color,color,0)
    drawer.Render()





    
while(1):
    time.sleep(.1)
    print_grid(drawer)
    pos= QPoint()
    if drawer.getLastMouseClick_R(pos):   
        while(1):
            pos= QPoint()
            if drawer.getLastMouseClick_R(pos) or drawer.getLastMouseClick_L(pos):
                break   
            iterate()
            print_grid(drawer)
            #time.sleep(.01)
    elif drawer.getLastMouseClick_L(pos):
        cell_array[int(pos.y()/block_size)][int(pos.x()/block_size)]=1
    
    
    