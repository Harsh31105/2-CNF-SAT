# Opening a file.
file = open("sampletext.txt", "r")
        
# Reading the file.
inputs = (file.read().replace(' ', '\n').splitlines())

# Converting the "text" data in the file to integer datatype. 
for i in range(0, len(inputs)):
    inputs[i] = int(inputs[i])

# Initializing a new list that will separately store my implications in one list. 
implications = []

# Converting Inputs to Implications. 
for i in range(0,len(inputs),2):
    implications.append(inputs[i]*-1)
    implications.append(inputs[i+1])
    implications.append(inputs[i+1]*-1)
    implications.append(inputs[i])

# Updating the numeral representations of the variables to include only positive numbers
# so it can be mapped out easier. 
for j in range(0, len(implications)):
    if implications[j] > 0:
        implications[j] = (implications[j]*2) - 1
    elif implications[j] < 0:
        implications[j] = abs(implications[j]*2)

length = len(implications)
rows = cols = int(max(implications))

# Initializing a 2-D Array that will store the implications in the form of a Matrix. 
arr = [[0 for i in range(cols)] for j in range(rows)]

#print(implications)

# Updating the "edges" into the Matrix. 
for k in range(0, length, 2):
    arr[implications[k]-1][implications[k+1]-1] = 1

# Prints the Matrix. 
#for i in range(0, rows):
    #for j in range(0, cols):
                   #print(str(arr[i][j]) + "  ", end="")
    #print('\n')

topological = []

""""""""""""""""""""""""""" Defining CNF2SAT """""""""""""""

from queue import LifoQueue

def CNF2SAT():

    stack = LifoQueue(maxsize=rows)

    visited = []
    for i in range(0, rows):
        visited.append(False)

    for j in range(0, rows):
        if (visited[j] == False):
            DFStart(j, visited, stack)

    transpose = makeTransposeMatrix()
    #print("Following are the SCCs:")
    
    for i in range(0, rows):
        visited[i] = False

    while (not stack.empty()):
        v = stack.get()
        temp = []
        
        if (visited[v] == False):
            DFSEnd(v, visited, transpose, temp)
            #print(temp)
            for m in range(0,len(temp)):
                for n in range(m+1 , len(temp)):
                    if (temp[m]%2==0 and temp[n]==temp[m]-1):
                        print("FALSE! Same pair detected within SCC!\nHence, assignment is not possible.")
                        exit()
                    elif (temp[m]%2==1 and temp[n]==temp[m]+1):
                        print("FALSE! Same pair detected within SCC!\nHence, assignment is not possible.")
                        exit()
            temp = []
            #print("\n")

    print("There exists a TRUE Assignment: ")

    print(topological)
    
    assignments = arr = [0 for i in range(rows)]

    # 0 -> Unassigned
    # 1 -> TRUE!
    # -1 -> FALSE!
    for p in range(0,rows):
        term = pair = 0
        if (topological[p]%2 == 0):
            term = assignments[topological[p]-1] #Indexed
            pair = assignments[topological[p]-2] #For Even values, checks the one before it as its "pair"
        elif (topological[p]%2 == 1):
            term = assignments[topological[p]-1]
            pair = assignments[topological[p]]


        #Checking if it is unassigned AND that its pair is unassigned. 
        if (term == 0 and pair == 0):
            assignments[topological[p]-1] = -1
        #Checking if it is unassigned AND that its pair is assigned, then assigns negation to it. 
        elif (term == 0 and pair != 0):
            assignments[topological[p]-1] = -pair

    for q in range(0,rows):
        print("Value for Node-",q+1,assignments[q]) 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""Defining DFS(Start)"""""""""""""""""""""""

def DFStart(v, visited, Stack):
    visited[v] = True
    for i in range(0,cols):
        if (arr[v][i] == 1 and (not visited[i])):
            DFStart(i, visited, Stack)
    Stack.put(v)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""Defining makeTransposeMatrix"""""

def makeTransposeMatrix():
    transpose = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(0, rows):
        for j in range(0, cols):
                   transpose[j][i] = arr[i][j];
    return transpose

""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""Defining DFS(End)"""""

def DFSEnd(v, visited, transpose, temp):
    visited[v] = True
    temp.append(v+1)
    topological.append(v+1)
    for i in range(0,cols):
        if (transpose[v][i] == 1 and (not visited[i])):
            DFSEnd(i, visited, transpose, temp)

""""""""""""""""""""""""""""""""""""""""""""""""""

CNF2SAT()

