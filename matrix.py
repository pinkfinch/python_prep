import copy


# NOTE: Please attempt to complete this hw without using additional modules such as numpy
class Matrix:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.storage = [[0 for col in range(n)] for row in range(m)]

    def printer(self):
        if not self.storage: return
        for i in self.storage:
            print(i)

    def isValid(self, i, j):
        if i >= 0 and i < self.m and j >= 0 and j < self.n: return True
        return False

    import copy
    def initialize(self, arrayOfArrays):
        if not arrayOfArrays: return
        self.storage = copy.deepcopy(arrayOfArrays)
        self.m = len(arrayOfArrays)
        self.n = len(arrayOfArrays[0])

    def insert(self, i, j, val):
        if self.isValid(i,j):
            self.storage[i][j] = val
            return True
        return False

    def retrieve(self, i, j):
        if self.isValid(i,j):
            return self.storage[i][j]
        return -float('inf')

    def scale(self, factor):
        self.storage = [[element*factor for element in row] for row in self.storage]

    def fill(self, val):
        self.storage = [[val]*self.n for _ in range(self.m)]

    def flatten(self):
        return [item for sublist in self.storage for item in sublist]

    def slice(self, rowRange, colRange):
        row_start = max(0, rowRange[0])
        row_end = min(self.m, rowRange[1])
        col_start = max(0, colRange[0])
        col_end = min(self.n, colRange[1])

        return [row[col_start:col_end] for row in self.storage[row_start:row_end]]

    def transpose(self):
        if not self.storage:
            return []
        return [[self.storage[row][col] for row in range(self.m)] for col in range(self.n)]

    def multiply(self, matrix):
        pass

test_count = [0, 0]
print('Slice Tests')
def test():
    matrix = Matrix(1, 1)
    matrix.initialize([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    newMatrix = matrix.slice([0,2], [0,2])

    return newMatrix != None and newMatrix.m == 2 and newMatrix.n == 2 and \
         newMatrix.storage[0][0] == 0 and newMatrix.storage[0][1] == 1 and \
         newMatrix.storage[1][0] == 3 and newMatrix.storage[1][1] == 4

test()