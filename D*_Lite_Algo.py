import heapq,math,random,time
import matplotlib.pyplot as plt

def make_grid(n,p,start,goal):
    while True:
        g=[[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if random.random()<p:
                    g[i][j]=1
        g[start[0]][start[1]]=0
        g[goal[0]][goal[1]]=0
        if bfs_check(g,start,goal):
            return g

def bfs_check(g,start,goal):
    n=len(g)
    q=[start]
    vis=set([start])
    while q:
        x,y=q.pop(0)
        if (x,y)==goal:
            return True
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<n and 0<=ny<n and g[nx][ny]==0 and (nx,ny) not in vis:
                vis.add((nx,ny))
                q.append((nx,ny))
    return False

def h(a,b):
    dr=abs(a[0]-b[0])
    dc=abs(a[1]-b[1])
    return math.sqrt(2)*min(dr,dc)+abs(dr-dc)

def neighbors(x,y,n):
    moves=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    res=[]
    for dx,dy in moves:
        nx,ny=x+dx,y+dy
        if 0<=nx<n and 0<=ny<n:
            res.append((nx,ny))
    return res

def cost(a,b):
    if a[0]!=b[0] and a[1]!=b[1]:
        return math.sqrt(2)
    return 1

def path_cost(path):
    c=0
    for i in range(1,len(path)):
        c+=cost(path[i-1],path[i])
    return c

def turns(path):
    t=0
    for i in range(2,len(path)):
        dx1=path[i-1][0]-path[i-2][0]
        dy1=path[i-1][1]-path[i-2][1]
        dx2=path[i][0]-path[i-1][0]
        dy2=path[i][1]-path[i-1][1]
        if (dx1,dy1)!=(dx2,dy2):
            t+=1
    return t

def dstar_lite(grid,start,goal):
    n=len(grid)
    g={}
    rhs={}
    U=[]
    in_queue=set()

    for i in range(n):
        for j in range(n):
            g[(i,j)]=float("inf")
            rhs[(i,j)]=float("inf")

    rhs[goal]=0
    heapq.heappush(U,(h(start,goal),0.0,goal))
    in_queue.add(goal)

    def calc_key(u):
        m=min(g[u],rhs[u])
        return (m+h(start,u),m)

    def update(u):
        if u!=goal:
            vals=[]
            for v in neighbors(u[0],u[1],n):
                if grid[v[0]][v[1]]==0:
                    vals.append(g[v]+cost(u,v))
            rhs[u]=min(vals) if vals else float("inf")

        in_queue.discard(u)

        if g[u]!=rhs[u]:
            k=calc_key(u)
            heapq.heappush(U,(k[0],k[1],u))
            in_queue.add(u)

    def compute():
        while U:
            k0,k1,u=U[0]
            ck=calc_key(start)
            if (k0,k1)>=(ck[0],ck[1]) and rhs[start]==g[start]:
                break
            heapq.heappop(U)
            if u not in in_queue:
                continue
            in_queue.discard(u)

            if g[u]>rhs[u]:
                g[u]=rhs[u]
                for v in neighbors(u[0],u[1],n):
                    update(v)
            else:
                g[u]=float("inf")
                update(u)
                for v in neighbors(u[0],u[1],n):
                    update(v)

    compute()

    path=[start]
    cur=start
    visited=set([start])

    while cur!=goal and len(path)<n*n*2:
        best=None
        minv=float("inf")

        for v in neighbors(cur[0],cur[1],n):
            if grid[v[0]][v[1]]==0:
                val=g[v]+cost(cur,v)
                if val<minv:
                    minv=val
                    best=v

        if best is None:
            return None

        cur=best
        path.append(cur)
        visited.add(cur)

        if random.random()<0.03:
            i=random.randint(0,n-1)
            j=random.randint(0,n-1)
            if (i,j)!=start and (i,j)!=goal and (i,j) not in visited:
                grid[i][j]=1-grid[i][j]
                update((i,j))
                for nb in neighbors(i,j,n):
                    if grid[nb[0]][nb[1]]==0:
                        update(nb)
                compute()

    return path

def plot(grid,path,start,goal):
    n=len(grid)
    img=[[1 if grid[i][j]==1 else 0 for j in range(n)] for i in range(n)]

    for x,y in path:
        img[x][y]=0.5

    img[start[0]][start[1]]=0.8
    img[goal[0]][goal[1]]=0.2

    plt.imshow(img)
    plt.title("D* Lite Navigation")
    plt.show()

def main():
    while True:
        try:
            n=int(input("Enter grid size: "))
            if n>0:
                break
        except ValueError:
            print("Invalid input")   
            

    while True:
        d=input("Enter density(low/medium/high): ").lower()
        if d in["low","medium","high"]:
            break

    while True:
        try:
            sx,sy=map(int,input("Enter start(x y): ").split())
            gx,gy=map(int,input("Enter goal(x y): ").split())
            if 0<=sx<n and 0<=sy<n and 0<=gx<n and 0<=gy<n:
                break
        except ValueError:
            print("Invalid input")   # was: pass

    p={"low":0.1,"medium":0.15,"high":0.25}[d]

    grid=make_grid(n,p,(sx,sy),(gx,gy))

    t0=time.time()
    path=dstar_lite(grid,(sx,sy),(gx,gy))
    t1=time.time()

    if path:
        pc=path_cost(path)
        dx=abs(sx-gx)
        dy=abs(sy-gy)
        straight=math.sqrt(dx*dx+dy*dy)
        ratio=pc/straight if straight!=0 else 1

        print("\nPath:",path)
        print("Path Cost:",round(pc,2))
        print("Steps:",len(path))
        print("Time:",round(t1-t0,4))
        print("Optimality Ratio:",round(ratio,3))
        print("Turns:",turns(path))

        plot(grid,path,(sx,sy),(gx,gy))
    else:
        print("Unexpected failure")

if __name__=="__main__":
    main()
