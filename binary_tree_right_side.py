'''
https://leetcode.com/problems/binary-tree-right-side-view/description/
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes
 you can see ordered from top to bottom.


Example 1:
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]
Explanation:

Example 2:
Input: root = [1,2,3,4,null,null,null,5]
Output: [1,3,4,5]
Explanation:


Example 3:
Input: root = [1,null,3]
Output: [1,3]

Example 4:
Input: root = []
Output: []
'''

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root: return []
        response = []
        q = deque([(root, 0)])
        prev_node = root
        prev_level = 0
        while q:
            node, level = q.popleft()
            if not node: return
            if level > prev_level:
                response.append(prev_node.val)
            if node.left:
                q.append((node.left,level+1))
            if node.right:
                q.append((node.right, level+1))
            prev_node, prev_level = node, level
        response.append(prev_node.val)
        return response