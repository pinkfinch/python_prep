# Given 2 BSTs, give the in-order traversal of the combined BST
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

def combined_bst(node1, node2):
    if not node1: return dfs(node2)
    if not node2: return dfs(node1)
    arr1, arr2 = [],[]

    def dfs(node, arr):
        if not node: return arr
        if node.left: dfs(node.left,arr)
        arr.append(node.val)
        if node.right: dfs(node.right, arr)
        return arr
    
    arr1 = dfs(node1, arr1)
    arr2 = dfs(node2, arr2)
    arr = []
    l,r = 0,0
    while l < arr1.length and r < arr2.length:
        if arr1[l] < arr2[r]:
            arr.append(arr1[l])
            l += 1
        elif arr1[l] > arr2[r]:
            arr.append(arr2[r])
            r += 1
    if l < arr1.length:
        arr.extend(arr1[l:arr1.length])
    else:
        arr.extend(arr2[r:arr2.length])
    return arr
