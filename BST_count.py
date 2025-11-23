# Number of Unique BST with N Keys
# Last Updated : 11 Jul, 2025
# Given an integer n, the task is to find the total number of unique BSTs that can be made using values from 1 to n.

# Examples:

# Input: n = 3
# Output: 5
# Explanation: For n = 3, preorder traversal of Unique BSTs are:
# 1 2 3
# 1 3 2
# 2 1 3
# 3 1 2
# 3 2 1


def num_bst(n):
    """
    Count unique BSTs using Catalan numbers
    dp[i] = number of unique BSTs with i nodes
    """
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty tree
    dp[1] = 1  # Single node
    
    for nodes in range(2, n + 1):
        for root in range(1, nodes + 1):
            left = root - 1
            right = nodes - root
            dp[nodes] += dp[left] * dp[right]
    
    return dp[n]

# Test
print(num_bst(3))  # Output: 5
print(num_bst(4))  # Output: 14
print(num_bst(5))  # Output: 42


