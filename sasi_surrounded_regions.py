"""
Do not return anything, modify board in-place instead.

Iterate through nodes and their neighbours to find the regions
If node is in perimeter then that whole region cannot be converted
While we visit the nodes, we mark them visited and dont revisit them
again
If the region is not in perimeter, we flip the region.
Loop through the entire board (not perimeters) and return.

"""


class Solution:

    def solve(self, board: List[List[str]]) -> None:

        m = len(board)
        n = len(board[0])
        visited = set()

        def get_neighbors(i, j):
            neighbors = set()
            di = [1, -1, 0, 0]
            dj = [0, 0, 1, -1]
            for k in range(len(di)):
                new_i = di[k] + i
                new_j = dj[k] + j
                if (
                        new_i < 0
                        or new_j < 0
                        or new_i == m
                        or new_j == n
                        or board[new_i][new_j] == "X"
                ): continue

                neighbors.add((new_i, new_j))
            return neighbors

        def dfs(i, j, found_perimeter, regions):
            if (i, j) in visited:
                return
            visited.add((i, j))

            if i <= 0 or j <= 0 or i >= m - 1 or j >= n - 1:
                found_perimeter[0] = True
            else:
                regions.add((i, j))

            neighbors = get_neighbors(i, j)
            for neighbor in neighbors:
                dfs(neighbor[0], neighbor[1], found_perimeter, regions)

        for i in range(0, m):
            for j in range(0, n):
                if (i, j) in visited:
                    continue
                if board[i][j] == "X":
                    continue
                if i == 0 or j == 0 or i == m - 1 or j == n - 1:
                    continue
                regions = set()
                found_perimeter = [False]
                dfs(i, j, found_perimeter, regions)
                print(i, j, regions, found_perimeter)
                if found_perimeter[0] == False:
                    for k, l in regions:
                        board[k][l] = 'X'

