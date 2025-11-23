class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        if left: self.left = left
        if right: self.right = right

    def print_node(self, node):
        if not node: return
        self.print_node(node.left)
        self.print_node(node.right)
        print(node.val)

class PostOrderDfs:

    def traverse(self, node, arr=None):
        if arr is None: arr = []
        if not node: return
        self.traverse(node.left,arr)
        self.traverse(node.right,arr)
        arr.append(node.val)
        return arr



    @classmethod
    def createPostOrderDfs(cls, arr, index=0):
        if not arr or len(arr) is None or index >= len(arr): return
        node = TreeNode(arr[index])
        node.left = cls.createPostOrderDfs(arr, 2*index + 1)
        node.right = cls.createPostOrderDfs(arr, 2*index + 2)
        return node


node = PostOrderDfs.createPostOrderDfs([22,2,3,1,3,3,33,45,66,88])
node.print_node(node)

p = PostOrderDfs()
arr = p.traverse(node)
print(arr)
