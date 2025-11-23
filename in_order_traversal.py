class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        if left: self.left = left
        if right: self.right = right

    def print_node(self, node):
        if not node: return
        self.print_node(node.left)
        print(node.val)
        self.print_node(node.right)

class InOrderDfs:

    def traverse(self, node):
        arr = []

        def inner(self, node, arr):
            if node is None: return
            inner(self, node.left, arr)
            arr.append(node.val)
            inner(self, node.right, arr)

        inner(self, node, arr)
        return arr

    @classmethod
    def createInOrderDfs(cls,arr, index=0):
        if arr is None or index >= len(arr):
            return None
        node = TreeNode(arr[index], None, None)
        node.left = cls.createInOrderDfs(arr, 2 * index + 1)
        node.right = cls.createInOrderDfs(arr, 2 * index + 2)
        return node

node = InOrderDfs.createInOrderDfs([23,3,33,22,34,55,5,66,98,22])
node.print_node(node)
d = InOrderDfs()
d.traverse(node)

