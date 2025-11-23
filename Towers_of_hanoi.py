'''
Towers of Hanoi
There are three vertical rods numbered 1, 2, and 3, and N disks with hollow centers that can slide over the rods.
Initially, the N disks are stacked on rod 1 in order of decreasing size, the smallest at the top,
thus approximating a conical shape.  The objective is to move the entire stack from rod 1 to rod 3,
obeying the following rules:[4]
1.     Only one disk may be moved at a time.
2.     Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack or
on an empty rod.
3.     No disk may be placed on top of a disk that is smaller than it.
Input: The number N of disks on the first rod
Output: List of pairs of numbers representing a solution to the problem. Each pair is two rods, the rod moved from
and the rod moved to.
Example:
N=2
Output: [ [1,2], [1,3], [2,3] ]

N=3
'''

def towers_of_hanoi(n):
    response = []

    def recurse(count, start, finish, free):
        if count == 1:
            response.append((start, finish))
            return

        recurse(count-1, start, free, finish)
        response.append((start, finish))
        recurse(count-1, free, finish, start)

    recurse(n,1, 3, 2)
    return response

print(towers_of_hanoi(2))
print(towers_of_hanoi(3))
print(towers_of_hanoi(4))

3,7,15,