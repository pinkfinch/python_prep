'''
https://leetcode.com/problems/network-delay-time/description/
You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as
directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time
it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal.
If it is impossible for all the n nodes to receive the signal, return -1.


Example 1:
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
Example 2:

Input: times = [[1,2,1]], n = 2, k = 1
Output: 1
Example 3:

Input: times = [[1,2,1]], n = 2, k = 2
Output: -1

Constraints:
1 <= k <= n <= 100
1 <= times.length <= 6000
times[i].length == 3
1 <= ui, vi <= n
ui != vi
0 <= wi <= 100
All the pairs (ui, vi) are unique. (i.e., no multiple edges.)

dijkstra's algorithm
1. first create adjacency matrix
2. create a minHeap to push elements into from the starting node k
3. push k into min heap with a weight of 0
    push its neighbors into min heap


4. pop from min-heap
    for each element - push into final list of elements.
    for each element, add the neighbors into the heap if not already in heap.
        when adding neighbor, weight = weight of neighbor + weight of node
        if node in captured, then dont add again

    return the weight of the last node.
'''
from typing import List
from queue import PriorityQueue

def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    pq = PriorityQueue()

    def createAdjacencyMatrix():
        matrix = {}
        for current, neighbor, weight in times:
            if current in matrix:
                matrix[current].append((neighbor, weight))
            else:
                matrix[current] = [(neighbor, weight)]
        return matrix

    matrix = createAdjacencyMatrix()
    distances = [float('inf')] * (n + 1)
    distances[0] = 0
    distances[k] = 0
    pq.put((0, k))
    while not pq.empty():
        current_distance, node = pq.get()
        if current_distance > distances[node]:
            continue

        if node in matrix:
            neighbors = matrix[node]
            for n, dist in neighbors:
                new_distance = dist+current_distance
                if new_distance < distances[n]:
                    distances[n] = new_distance
                    pq.put((new_distance, n))
    print(distances)
    max_dist = max(distances)
    return max_dist if max_dist != float('inf') else -1

print(networkDelayTime([[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2))  #2
print(networkDelayTime([[1,2,1]], n = 4, k = 2))    #-1
print(networkDelayTime([[1,2,1],[2,1,3]], n = 2, k = 2))  #3
print(networkDelayTime([[1,2,1],[2,3,2],[1,3,4]],3,1)) #3
print(networkDelayTime([[1,2,1],[2,3,2],[1,3,1]],3,2))




