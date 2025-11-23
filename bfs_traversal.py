from collections import deque

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def print_node(self):
        def inner(node):
            if not node: return
            print(node.val)
            inner(node.left)
            inner(node.right)
        inner(self)


class BreadthFirst:

    # def bfs(self,node):
    #     arr = []
    #     if not node: return []
    #     q = queue.Queue()
    #     q.put(node)
    #     while not q.empty():
    #         el = q.get()
    #         arr.append(el.val)
    #         if el.left: q.put(el.left)
    #         if el.right: q.put(el.right)

    #     return arr

    def bfs(self, node):
        if not node: return []
        q = deque([node])
        arr = []
        while q:
            node = q.popleft()
            arr.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        return arr


    @classmethod
    def createBfsTree(cls, array, index=0):
        if not array or index >= len(array): return
        node = TreeNode(array[index])
        node.left = BreadthFirst.createBfsTree(array, 2*index+1)
        node.right = BreadthFirst.createBfsTree(array, 2*index + 2)
        return node

node = BreadthFirst.createBfsTree([4,2,5,1,3,7,6,8])
node.print_node()

b = BreadthFirst()
arr = b.bfs(node)
print(arr)
