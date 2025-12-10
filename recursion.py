#lattice paths. given a lattice of M*N squares, count number of unique paths from top left corner to bottom right. 
#you can only go to adjacent square right or down

def latticePaths(m,n):
    currentx, currenty = 0, 0
    paths = 0
    def recurse(x, y, paths):
        if x >= m or y >= n:
            return
        if x == m-1 and y == n-1:
            return paths
        recurse(x+1, y, paths+1)


