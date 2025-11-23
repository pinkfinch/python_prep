class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right

    def print_tree(self, node):
        if node is None: return
        print(node.val)
        self.print_tree(node.left)
        self.print_tree(node.right)

class PreOrderDfs:

    def __init__(self, node):
        self.node = node

    def traverse(self, root, arr):
        current = root
        if arr is None: arr = []
        if root is None: return arr
        arr.append(current.val)
        self.traverse(current.left, arr)
        self.traverse(current.right, arr)
        return arr

    @classmethod
    def createPreOrderDfs(cls,arr, index=0):
        # Builds binary tree from array using level-order mapping:
        # left = 2*i + 1, right = 2*i + 2
        if arr is None or index >= len(arr):
            return None
        node = TreeNode(arr[index],None, None)
        node.left = cls.createPreOrderDfs(arr, 2 * index + 1)
        node.right = cls.createPreOrderDfs(arr, 2 * index + 2)
        return node


root = PreOrderDfs.createPreOrderDfs([1,2,3,4,45,66,7,9])
root.print_tree(root)

p = PreOrderDfs(root)
print(p.traverse(root, []))
