'''
332. Reconstruct Itinerary
https://leetcode.com/problems/reconstruct-itinerary/description/
You are given a list of airline tickets where tickets[i] = [fromi, toi] represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.

All of the tickets belong to a man who departs from "JFK", thus, the itinerary must begin with "JFK". If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string.

For example, the itinerary ["JFK", "LGA"] has a smaller lexical order than ["JFK", "LGB"].
You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.

Example 1:
Input: tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
Output: ["JFK", "MUC", "LHR", "SFO", "SJC"]

Example 2:
Input: tickets = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
Output: ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]
Explanation: Another possible reconstruction is ["JFK", "SFO", "ATL", "JFK", "ATL", "SFO"] but
it is larger in lexical order.

Constraints:
1 <= tickets.length <= 300
tickets[i].length == 2
from[i].length == 3
to[i].length == 3
fromi and toi consist of uppercase English letters.
fromi != toi

map[start]= end or map[start] = [end1, end2]
end1, end2 to be in sorted order
src = 'JFK'
while map:
  if i == 0 list.append(src)
  dest = map[src]
  if dest.length > 0
    list.append(dest[0])
    dest.remove(dest[0])
  else
    list.append(dest)
    map.remove(src)
return list
'''


from heapq import *
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        tickets.sort(reverse=True)
        map = {}
        for ticket in tickets:
            if ticket[0] in map:
                map[ticket[0]].append(ticket[1])
            else:
                map[ticket[0]] = [ticket[1]]
        print(map)
        routes = []
        def visit(airport):
            while airport in map and map[airport]:
                next_dest = map[airport].pop()
                visit(next_dest)
            routes.append(airport)

        visit('JFK')
        routes.reverse()
        return routes

s = Solution()
# print(s.findItinerary([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]))
# print(s.findItinerary([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]))
print(s.findItinerary([["JFK","SFO"],["JFK","ATL"],["SFO","JFK"],["ATL","AAA"],["AAA","ATL"]]))