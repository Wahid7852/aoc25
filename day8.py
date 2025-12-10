boxes=[]
with open('inputs/day8_input.txt') as f:
    for line in f:
        if line.strip():
            x,y,z=map(int,line.split(','))
            boxes.append((x,y,z))
N=len(boxes)

pairs=[]
for i in range(N-1):
    x1,y1,z1=boxes[i]
    for j in range(i+1,N):
        x2,y2,z2=boxes[j]
        d=(x1-x2)**2+(y1-y2)**2+(z1-z2)**2
        pairs.append((d,i,j))

pairs.sort(key=lambda x:x[0])
len(pairs)

parent=list(range(N))
size=[1]*N

def find(a):
    while parent[a]!=a:
        parent[a]=parent[parent[a]]
        a=parent[a]
    return a

def union(a,b):
    ra,rb=find(a),find(b)
    if ra==rb: return size[ra]
    if size[ra]<size[rb]: ra,rb=rb,ra
    parent[rb]=ra
    size[ra]+=size[rb]
    return size[ra]

M=1000
for k in range(M):
    _,i,j=pairs[k]
    union(i,j)

comps={}
for i in range(N):
    r=find(i)
    comps.setdefault(r,0)
    comps[r]+=1
sizes=sorted(comps.values(), reverse=True)
part1 = sizes[0]*sizes[1]*sizes[2]

full= None
for k in range(M, len(pairs)):
    _,i,j=pairs[k]
    s=union(i,j)
    if s==N:
        full = boxes[i][0]*boxes[j][0]
        break

print(part1, full)