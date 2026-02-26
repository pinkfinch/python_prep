# Maximum number of employees
# You are given a list of time cards. Each card contains a start time and end time for an employee (times are given as positive integers). Determine the maximum number of employees who are working simultaneously.
# Example 1:
# Input: [ [1,5], [2,3], [4,7] ]
# Output: 2
# Explanation: There are two employees working at times 2, 3, 4, and 5. Fewer employers are working at all other times.
# Example 2:
# Input: [ [1,5], [6,10] ]
# Output: 1
# Explanation: There is one employee working at each of the times 1 through 10. No employees are working at other times.
# Constraints:
# N is number of time cards in the list
# Time: O(N log N)
# Auxiliary Space: O(N)
# Details
# -          End times will always be at or after the corresponding start times
# -          You can assume that the input is in the correct format
# -          You cannot assume that the list is sorted
# -          Integers will fit in standard 32 bit ints
# -          The list can be empty
"""
i, j
start with i - go through the list, while value < end - keep adding to the number of elements
since 2 < 5 we incr count
  sort by start time, min heap of end time

  so as we go through - start at the first el
  incr worker count, update max_count
  go to second el, peek at heap, and see if it is < the second el - if so, pop it and and decr count
  otherwise keep going

two lists - one sorted by start time, one sorted by end time
if we hit a new start time, we add count. if count > max, update max
if we hit end time, we decrement count
"""
import heapq
def max_num_employees(timeslots):

    sorted1 = sorted(timeslots)
    end_times = [x[1] for x in timeslots]
    heapq.heapify(end_times)
    current_ct = 0
    max_ct = 0

    for k in range(0, len(sorted1)):
        start = sorted1[k][0]
        while start >= end_times[0]:
            heapq.heappop(end_times)
            current_ct -= 1
        current_ct += 1
        max_ct = max(current_ct, max_ct)
    return max_ct


print(max_num_employees([ [1,5], [2,3], [4,7] ]))
print(max_num_employees([ [1,5], [2,5], [3,7] ]))

print(max_num_employees([ [1,8], [2,5], [3,7],[5,9],[10,11] ]))

# 1 2 3 4 5 6 7 8 9 10 11
# ---------------
#   -------
#     --------
#         --------



