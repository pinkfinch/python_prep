# find the difference between the odd level numbers and even level numbers
from collections import deque

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def print_node(self, node):
        if not node: return
        self.print_node(node.left)
        print(node.val)
        self.print_node(node.right)

class Dfs:

    def __init__(self):
        self.odd_sum = 0
        self.even_sum = 0

    def traverse(self, node, height):
        if not node: return
        if height % 2 == 0:
            self.even_sum += node.val
        else:
            self.odd_sum += node.val

        self.traverse(node.left, height+1)
        self.traverse(node.right, height+1)
        return self.odd_sum - self.even_sum


    @classmethod
    def createDfs(cls, arr, index=0):
        if not arr or len(arr) is None or index >= len(arr): return
        node = TreeNode(arr[index])
        node.left = cls.createDfs(arr, 2*index + 1)
        node.right = cls.createDfs(arr, 2*index + 2)
        return node


class Bfs:

    def traverse(self,root):
        if not root: return 0
        q = deque([root])
        level = {root: 1}
        sum = 0
        while q:
            current = q.popleft()
            if level[current] % 2 == 0:
                sum -= current.val
            else:
                sum += current.val
            if current.left:
                q.append(current.left)
                level[current.left] = level[current] + 1
            if current.right:
                q.append(current.right)
                level[current.right] = level[current] + 1
        return sum





node = Dfs.createDfs([10,20,30,40,50,60])
node.print_node(node)

d = Dfs()
print(d.traverse(node, 1))

b = Bfs()
print(b.traverse(node))
