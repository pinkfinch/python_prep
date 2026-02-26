'''

Question 1: Supply Chain Depth Calculator (Graph Traversal)Problem:
Given a supply chain network where companies source from suppliers, find the maximum depth of the supply chain for a given product.
python# Input: adjacency list representing supplier relationships
supply_chain = {
    "iPhone": ["Foxconn"],
    "Foxconn": ["TSMC", "Samsung Display"],
    "TSMC": ["ASML", "Applied Materials"],
    "Samsung Display": ["Corning Glass"],
    "ASML": ["Zeiss"],
    "Applied Materials": [],
    "Corning Glass": [],
    "Zeiss": []
}
# Output: 4 (iPhone -> Foxconn -> TSMC -> ASML -> Zeiss)Requirements:

Calculate the longest path from product to raw materials
Handle cycles (return -1 if circular dependency detected)
Return all companies at the maximum depth level

Follow-ups:
What if we want to find the shortest path instead (critical path analysis)?
How would you modify this to calculate total cost if each edge has a cost?
What if the graph has 10M nodes - how do you optimize?
Concepts tested: DFS/BFS, cycle detection, graph traversal, memoization
'''

# Using DFS - to search all the paths and find the deepest path to supply chain

def find_longest_path(supply_chain):
    longest_depth = 0
    visited = set()
    path = []
    longest_path = []
    def dfs(node, depth, path):
        nonlocal longest_depth, longest_path
        if depth > longest_depth:
            longest_depth = depth
            longest_path[:] = path[:]
        if not node:
            return

        for n in supply_chain[node]:
            if n in visited:
                return depth
            visited.add(n)
            path.append(node)
            dfs(n, depth+1, path)
            visited.remove(n)
            path.remove(node)

    start = list(supply_chain.keys())[0]
    visited.add(start)
    path = [start]
    dfs(start, 0, path)
    return longest_path

supply_chain = {
    "iPhone": ["Foxconn"],
    "Foxconn": ["TSMC", "Samsung Display"],
    "TSMC": ["ASML", "Applied Materials"],
    "Samsung Display": ["Corning Glass"],
    "ASML": ["Zeiss"],
    "Applied Materials": [],
    "Corning Glass": [],
    "Zeiss": []
}
print(find_longest_path(supply_chain))




