from sys import argv
from copy import deepcopy
from queue import Queue
import heapq

class Node:
    def __init__(self, node, parent, schild, cost):
        self.node = node
        self.parent = parent
        self.schild = schild
        self.cost = cost
        self.priority = None
        self.mismatch = 9
        self.manhattanD = 0
    def __lt__(self, other):
        return self.priority < other.priority


class PQueue:
    def __init__(self):
        self.queue = []
    def push1(self, node, cost):
        heapq.heappush(self.queue, (cost, node))
    def push2(self, node, mismatch):
        heapq.heappush(self.queue, (mismatch, node))
    def push3(self, node, manhattanD):
        heapq.heappush(self.queue, (manhattanD, node))
    def pop(self):
        return heapq.heappop(self.queue)[-1]
    

def bfs(start, end):
    frontier = Queue()
    frontier.put(start)
    explored = []
    pathcost = 0
    discovered = 0
    expanded = 0
    while not(frontier.empty()):
        current = frontier.get()
        if is_goal(current, end):
            pathcost = path_generator(end, pathcost)
            return path_output(start, pathcost, discovered, expanded)
        explored.append(current)
        expanded += 1
        expand_nodes = expand(current, end)
        while not(expand_nodes.empty()):
            n = expand_nodes.get()
            if (n not in frontier.queue) and (n not in explored):
                frontier.put(n)
                discovered += 1               
    return no_solution(pathcost, discovered, expanded)
    

def ucost(start, end):
    frontier = PQueue()
    frontier.push1(start, start.cost)
    explored = []
    pathcost = 0
    discovered = 0
    expanded = 0
    while frontier:
        current = frontier.pop()
        if is_goal(current, end):
            pathcost = path_generator(end, pathcost)
            return path_output(start, pathcost, discovered, expanded)
        explored.append(current.node)
        expanded += 1
        expand_nodes = expand(current, end)
        while not(expand_nodes.empty()):
            n = expand_nodes.get()
            if (n not in frontier.queue) and (n.node not in explored):
                frontier.push1(n, n.cost)
                discovered += 1
    return no_solution(pathcost, discovered, expanded)


def greedy(start, end):
    frontier = PQueue()
    frontier.push2(start, start.mismatch)
    explored = []
    pathcost = 0
    discovered = 0
    expanded = 0
    while frontier:
        current = frontier.pop()
        if is_goal(current, end):
            pathcost = path_generator(end, pathcost)
            return path_output(start, pathcost, discovered, expanded)
        explored.append(current.node)
        expanded += 1
        expand_nodes = expand(current, end)
        while not(expand_nodes.empty()):
            n = expand_nodes.get()
            if (n not in frontier.queue) and (n.node not in explored):
                frontier.push2(n, n.mismatch)
                discovered += 1
    return no_solution(pathcost, discovered, expanded)


def astar(start, end):
    frontier = PQueue()
    frontier.push3(start, start.manhattanD)
    explored = []
    pathcost = 0
    discovered = 0
    expanded = 0
    while frontier:
        current = frontier.pop()
        if is_goal(current, end):
            pathcost = path_generator(end, pathcost)
            return path_output(start, pathcost, discovered, expanded)
        explored.append(current.node)
        expanded += 1
        expand_nodes = expand(current, end)
        while not(expand_nodes.empty()):
            n = expand_nodes.get()
            if (n not in frontier.queue) and (n.node not in explored):
                frontier.push3(n, n.manhattanD)
                discovered += 1
    return no_solution(pathcost, discovered, expanded)


def expand(current, end):
    node = current.node
    gnode = end.node
    moves = ['left','right','up','down']
    nodes = Queue()
    ii = 0
    jj = 0
    mismatch = 9

    for i in range(3):
        for j in range(3):
            if node[i][j] == '.':
                ii = i
                jj = j
                if i == 0:
                    moves.remove('up')
                elif i == 2:
                    moves.remove('down')
                if j == 0:
                    moves.remove('left')
                elif j == 2:
                    moves.remove('right')           
            if node[i][j] == gnode[i][j]:
                mismatch -= 1
    current.mismatch = mismatch
    current.manhattanD = manhattan_distance(current)
    
    for move in moves:
        newNode = deepcopy(node)
        if(move == 'left'):
            newNode[ii][jj], newNode[ii][jj-1] = newNode[ii][jj-1], newNode[ii][jj]
            child = Node(newNode, current, None, current.cost + int(newNode[ii][jj]))
            child.priority = int(newNode[ii][jj])
            if newNode[ii][jj] == gnode[ii][jj]:
                child.mismatch -= 1
            if newNode[ii][jj-1] == gnode[ii][jj-1]:
                child.mismatch -= 1
            child.manhattanD = manhattan_distance(child)
            nodes.put(child)
        elif(move == 'right'):
            newNode[ii][jj], newNode[ii][jj+1] = newNode[ii][jj+1], newNode[ii][jj]
            child = Node(newNode, current, None, current.cost + int(newNode[ii][jj]))
            child.priority = int(newNode[ii][jj])
            if newNode[ii][jj] == gnode[ii][jj]:
                child.mismatch -= 1
            if newNode[ii][jj+1] == gnode[ii][jj+1]:
                child.mismatch -= 1
            child.manhattanD = manhattan_distance(child)
            nodes.put(child)
        elif(move == 'up'):
            newNode[ii][jj], newNode[ii-1][jj] = newNode[ii-1][jj], newNode[ii][jj]
            child = Node(newNode, current, None, current.cost + int(newNode[ii][jj]))
            child.priority = int(newNode[ii][jj])
            if newNode[ii][jj] == gnode[ii][jj]:
                child.mismatch -= 1
            if newNode[ii-1][jj] == gnode[ii-1][jj]:
                child.mismatch -= 1
            child.manhattanD = manhattan_distance(child)
            nodes.put(child)
        elif(move == 'down'):
            newNode[ii][jj], newNode[ii+1][jj] = newNode[ii+1][jj], newNode[ii][jj]
            child = Node(newNode, current, None, current.cost + int(newNode[ii][jj]))
            child.priority = int(newNode[ii][jj])
            if newNode[ii][jj] == gnode[ii][jj]:
                child.mismatch -= 1
            if newNode[ii+1][jj] == gnode[ii+1][jj]:
                child.mismatch -= 1
            child.manhattanD = manhattan_distance(child)
            nodes.put(child)
    return nodes


def manhattan_distance(current):
    node = current.node
    manhattanD = 0
    for i in range(3):
        for j in range(3):
            if node[i][j] == '1':
                manhattanD += abs(i - 0) + abs(j - 1)
            elif node[i][j] == '2':
                manhattanD += abs(i - 0) + abs(j - 2)
            elif node[i][j] == '3':
                manhattanD += abs(i - 1) + abs(j - 0)
            elif node[i][j] == '4':
                manhattanD += abs(i - 1) + abs(j - 1)
            elif node[i][j] == '5':
                manhattanD += abs(i - 1) + abs(j - 2)
            elif node[i][j] == '6':
                manhattanD += abs(i - 2) + abs(j - 0)
            elif node[i][j] == '7':
                manhattanD += abs(i - 2) + abs(j - 1)
            elif node[i][j] == '8':
                manhattanD += abs(i - 2) + abs(j - 2)
    return manhattanD
    

def is_goal(current, target):
    if(current.node == target.node):
        target.parent = current.parent
        target.priority = current.priority
        return True
    else:
        return False


def path_generator(node, cost):
    rpath = Queue()
    rpath.put(node)
    while not(rpath.empty()):
        rcurrent = rpath.get()
        rparent = rcurrent.parent
        tempcur = rcurrent.node
        if rparent is not None:
            rparent.schild = rcurrent
            temppar = rparent.node
            rpath.put(rparent)
            for i in range(3):
                for j in range(3):
                    if temppar[i][j] != tempcur[i][j]:
                        if temppar[i][j] != '.':
                            tempcost = int(temppar[i][j])
                        else:
                            tempcost = int(tempcur[i][j])
                        cost += tempcost
    cost /= 2
    return int(cost)


def path_output(node, cost, frontier, expand):
    path = Queue()
    path.put(node)
    while not(path.empty()):
        state = path.get()
        print(state.node[0][0] + ' ' + state.node[0][1] + ' ' + state.node[0][2])
        print(state.node[1][0] + ' ' + state.node[1][1] + ' ' + state.node[1][2])
        print(state.node[2][0] + ' ' + state.node[2][1] + ' ' + state.node[2][2])
        print('')
        if state.schild is not None:           
            path.put(state.schild)
    print('path cost: ' + str(cost))
    print('frontier: ' + str(frontier))
    print('expanded: ' + str(expand))


def no_solution(cost, frontier, expand):
    print("No solution")
    print('path cost: ' + str(cost))
    print('frontier: ' + str(frontier))
    print('expanded: ' + str(expand))


def main():
    board = []
    tempb = []
    method = argv[1]
    goal = [['.', '1', '2'],['3','4','5'],['6','7','8']]
    end = Node(goal, None, None, 0)

    with open(argv[2], 'r') as f:
        for line in f:
          tempb = line.split()
          board.append(tempb)
    start = Node(board, None, None, 0)
    
    if method == 'bfs':
        bfs(start, end)
    elif method == 'ucost':
        ucost(start, end)
    elif method == 'greedy':
        greedy(start, end)
    elif method == 'astar':
        astar(start, end)

if __name__ == "__main__":
    main()
