import heapq
import random
import math
import time
import matplotlib.pyplot as plt

def generateGrid(n, density):
    grid=[[0 for _ in range(n)] for _ in range(n)]
    prob={"low": 0.1, "medium": 0.2, "high": 0.3}[density]
    count=0
    for i in range(n):
        for j in range(n):
            if random.random() < prob:
                grid[i][j]=1
                count+=1
    return grid, count / (n*n)

def valid(x, y, n, grid):
    return 0 <= x < n and 0 <= y < n and grid[x][y] == 0

def h(a, b):
    dx=abs(a[0] - b[0])
    dy=abs(a[1] - b[1])
    return (dx+dy)+(math.sqrt(2)-2)*min(dx,dy)

def astar(grid,start,goal):
    n=len(grid)
    pq=[]
    heapq.heappush(pq,(0,start))
    g={start: 0}
    parent={start: None}
    visited=set()
    nodes=0

    moves=[
        (1,0,1),(-1,0,1),(0,1,1),(0,-1,1),
        (1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),
        (-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))
    ]

    while pq:
        f,cur=heapq.heappop(pq)
        if cur in visited:
            continue
        visited.add(cur)
        nodes+=1

        if cur==goal:
            path=[]
            while cur:
                path.append(cur)
                cur=parent[cur]
            return path[::-1], nodes, g[goal]

        x,y=cur
        for dx,dy,cost in moves:
            nx,ny=x+dx,y+dy
            if valid(nx,ny,n,grid):
                newg=g[(x,y)]+cost
                if (nx,ny) not in g or newg < g[(nx,ny)]:
                    g[(nx,ny)]=newg
                    heapq.heappush(pq, (newg+h((nx,ny),goal),(nx,ny)))
                    parent[(nx,ny)]=(x,y)

    return None, nodes, float("inf")

def getTurns(path):
    if len(path) < 3:
        return 0
    turns=0
    for i in range(2, len(path)):
        dx1=path[i-1][0]-path[i-2][0]
        dy1=path[i-1][1]-path[i-2][1]
        dx2=path[i][0]-path[i-1][0]
        dy2=path[i][1]-path[i-1][1]
        if (dx1, dy1) != (dx2, dy2):
            turns+=1
    return turns

def plot(grid, path, start, goal):
    n=len(grid)
    img=[[1 if grid[i][j]==1 else 0 for j in range(n)] for i in range(n)]

    for (x,y) in path:
        img[x][y] = 0.5

    sx,sy=start
    gx,gy=goal
    img[sx][sy]=0.8
    img[gx][gy]=0.2

    plt.imshow(img)
    plt.title("UGV Navigation")
    plt.show()

def main():
    while True:
        try:
            n=int(input("Enter grid size: "))
            if n > 0:
                break
        except ValueError:
            print("Invalid input")

    while True:
        density=input("Enter density (low/medium/high): ").lower()
        if density in ["low","medium","high"]:
            break
        print("Invalid density")

    while True:
        try:
            sx,sy=map(int, input("Enter start (x y): ").split())
            gx,gy=map(int, input("Enter goal (x y): ").split())
            if 0 <= sx < n and 0 <= sy < n and 0 <= gx < n and 0 <= gy < n:
                break
        except ValueError:
            pass
        print("Invalid coordinates")

    grid, obstacle_density = generateGrid(n, density)
    grid[sx][sy]=0
    grid[gx][gy]=0

    start_time=time.time()
    path, nodes, cost=astar(grid, (sx, sy), (gx, gy))
    end_time=time.time()

    if path:
        dx=abs(sx - gx)
        dy=abs(sy - gy)
        straight=math.sqrt(dx*dx + dy*dy)
        ratio=cost/straight if straight != 0 else 1

        print("\nPath:", path)
        print("Path Cost:", round(cost,2))
        print("Nodes Expanded:", nodes)
        print("Computation Time:", round(end_time-start_time,4),"sec")
        print("Straight Line Distance:", round(straight,2))
        print("Optimality Ratio:", round(ratio,3))
        print("Direction Changes:", getTurns(path))
        print("Obstacle Density:", round(obstacle_density,3))
        print("Search Coverage:", round(nodes/(n*n),3))

        plot(grid, path, (sx, sy), (gx, gy))
    else:
        print("No path found")
        
main()
