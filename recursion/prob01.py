path = 'input.txt'
with open(path, 'r') as f:
    N = int(f.readline())
    brd = []
    for _ in range(N):
        line = f.readline()
        brd.append([int(v) for v in line.split(' ')])

    s = [int(v) for v in f.readline().split(' ')]
    t = [int(v) for v in f.readline().split(' ')]



def inside(p):
    return 0 <= p[0] < N and 0 <= p[1] < N


offset = [[-1, 0],
          [0, 1],
          [1, 0],
          [0, -1]]

def move(p, d):
    p[0] += offset[d][0]
    p[1] += offset[d][1]
    return p

def navigate(cur):
    if not inside(cur) or brd[cur[0]][cur[1]] != 0:
        return False;
    if cur == t:
        return True

    brd[cur[0]][cur[1]] = 2
    for d in range(4):
        #print("d = %d" % d)
        count = 0
        p = cur.copy()
        for i in range(N):
            #print("i = %d" % i)
            p = move(p, d)
            if not inside(p):
                break
            if brd[p[0]][p[1]] == 1:
                count += 1
                if count > 1:
                    break
            if count == 1 and brd[p[0]][p[1]] == 0:
                if navigate(p):
                    return True
    brd[cur[0]][cur[1]] = 3
    return False

if navigate(s) ==  True:
    print("Yes")
print("No")