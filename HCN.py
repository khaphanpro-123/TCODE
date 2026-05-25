M, N = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(M)]
visited = [[0]*N for _ in range(M)]

dx = [1,-1,0,0]
dy = [0,0,1,-1]

def dfs(i,j):
    stack=[(i,j)]
    visited[i][j]=1
    comp=[]
    while stack:
        x,y=stack.pop()
        comp.append((x,y))
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if 0<=nx<M and 0<=ny<N and a[nx][ny]==1 and not visited[nx][ny]:
                visited[nx][ny]=1
                stack.append((nx,ny))
    return comp

def is_rectangle(comp):
    xs=[x for x,y in comp]
    ys=[y for x,y in comp]
    x1,x2=min(xs),max(xs)
    y1,y2=min(ys),max(ys)
    area=(x2-x1+1)*(y2-y1+1)
    return len(comp)==area, x1,x2,y1,y2

def is_type2(x1,x2,y1,y2):
    # check viền
    for i in range(x1,x2+1):
        if a[i][y1]!=1 or a[i][y2]!=1:
            return False
    for j in range(y1,y2+1):
        if a[x1][j]!=1 or a[x2][j]!=1:
            return False

    # đếm vùng 0
    seen=[[0]*N for _ in range(M)]
    cnt=0
    for i in range(x1+1,x2):
        for j in range(y1+1,y2):
            if a[i][j]==0 and not seen[i][j]:
                cnt+=1
                stack=[(i,j)]
                seen[i][j]=1
                while stack:
                    x,y=stack.pop()
                    for k in range(4):
                        nx,ny=x+dx[k],y+dy[k]
                        if x1<nx<x2 and y1<ny<y2 and a[nx][ny]==0 and not seen[nx][ny]:
                            seen[nx][ny]=1
                            stack.append((nx,ny))
    return cnt==1

total=type1=type2=0

for i in range(M):
    for j in range(N):
        if a[i][j]==1 and not visited[i][j]:
            comp=dfs(i,j)
            ok,x1,x2,y1,y2=is_rectangle(comp)

            if ok:
                total+=1
                type1+=1
            elif is_type2(x1,x2,y1,y2):
                total+=1
                type2+=1

print(total)
print(type1)
print(type2)