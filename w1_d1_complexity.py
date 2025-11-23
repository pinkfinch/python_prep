#
#  Homework - Complexity
#
#
#  For the following functions, write the expected Time and Auxiliary Space
#  Complexity using what you know about nested loops, hash table look-ups and
#  the runtime of built in functions.
#
#  NOTE: You don't need to code to anything for these problems, just write
#  what you the complexity to be using big-O notation
#

#   Order of Magnitude
#
#   Reduce the following into it's Big-O order of magnitude.
#
#  1. 5 + N                    // N
#  2. N + N^2                  // N^2
#  3. 15N + 13N                // N
#  4. 10000                    // 1
#  5. log(N) + 1               // log(N)
#  6. log(N) * 3 + 14N + 3     // N
#  7. Nlog(N) + 3N^2           // N^2
#  8. N^3 + log(N^4)           // N^3
#  9. N! + 180000N^2           // N!
#  10. 15002^N                 // 15002^N

#    Index Of
#
#    Given an array of integers and a target value, return the index of the first
#    element that matches the target value. If there are no matches, return -1.
#
#    Parameters
#    Input: arr {Array of Integers}
#    Input: target {Integer}
#    Output: {Integer}
#
#    Examples
#    [1, 2, 3, 4, 5, 6], 5 --> 4
#    [9, 83, 74], 8 --> -1
#    [6, 4, 7, 9, 7, 8, 2, 4, 3], 7 --> 2

# Time Complexity:    O(N)
# Auxiliary Space Complexity: O(1)

def index_of(arr, target):
    for i in range(len(arr)):
        if arr[i] == target: return i
    return -1


print(index_of([1, 2, 3, 4, 5, 6], 5)) # 4
print(index_of([9, 83, 74], 8)) # -1
print(index_of([6, 4, 7, 9, 7, 8, 2, 4, 3], 7)) #2

#    Evens
#
#    Given an array of integers, return an array of only the even values.
#
#    Parameters
#    Input: arr {Array of Integers}
#    Output: {Array of Integers}
#
#    Examples
#    [1, 2, 3, 4, 5, 6] --> [2, 4, 6]
#    [9, 83, 74] --> [74]
#    [6, 4, 7, 9, 7, 8, 2, 4, 3] --> [6, 4, 8, 2, 4]

# Time Complexity: O(N)
# Auxiliary Space Complexity: O(1)

def evens(arr):
    new_arr = []
    for i in arr:
        if i % 2 == 0: new_arr.append(i)
    return new_arr


print(evens([1, 2, 3, 4, 5, 6])) # [2, 4, 6]
print(evens([9, 83, 74])) # [74]
print(evens([6, 4, 7, 9, 7, 8, 2, 4, 3])) # [6, 4, 8, 2, 4]

#   Sum
#
#   Given an array of integers, return the sum of all the integers.
#
#   Parameters
#   Input: arr {Array of Integers}
#   Output: {Integer}
#
#   Examples
#   [1, 2, 3, 4, 5] --> 15
#   [0, 1, -1] --> 0
#   [] --> 0
#
# Time Complexity: O(N)
# Auxiliary Space Complexity: O(1)

def sum(arr):
    sum = 0
    for i in arr:
        sum += i
    return sum


print(sum([1, 2, 3, 4, 5])) # 15
print(sum([0, 1, -1])) # 0
print(sum([])) # 0

#   Merge Arrays

#   Given two sorted arrays of integers, return a merged sorted array of both inputs.
#
#   Parameters
#   Input: arr1 {Array of Integers}
#   Input: arr2 {Array of Integers}
#   Output: {Array of Integers}
#
#   Examples
#   [1, 3, 9], [2, 4, 8] --> [1, 2, 3, 4, 8, 9]
#   [12, 25, 40], [20, 37, 45] --> [12, 20, 25, 37, 40, 45]
#   [10, 13, 24], [12, 35] --> [10, 12, 13, 24, 25]
#
# Time Complexity: O(N+M)
# Auxiliary Space Complexity:O(1)

def merge_arrays(arr1, arr2):
    if arr1 is None or len(arr1) == 0: return arr2
    if arr2 is None or len(arr2) == 0: return arr1
    arr = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            arr.append(arr1[i])
            i += 1
        elif arr1[i] > arr2[j]:
            arr.append(arr2[j])
            j += 1
        else:
            arr.append(arr1[i])
            arr.append(arr2[j])
            i += 1
            j += 1

    while i < len(arr1):
        arr.append(arr1[i])
        i += 1
    while j < len(arr2):
        arr.append(arr2[j])
        j += 1
    return arr

print(merge_arrays([1, 3, 9], [2, 4, 8])) # [1, 2, 3, 4, 8, 9]
print(merge_arrays([12, 25, 40], [20, 37, 45])) # [12, 20, 25, 37, 40, 45]
print(merge_arrays([10, 13, 24], [12, 35])) # [10, 12, 13, 24, 25]

#    Factorial
#
#    Given an input integer n, return the n factorial value.
#
#    Parameters
#    Input: n {Integer}
#    Output: {Integer}
#
#   Examples
#   5  --> 120 (5 * 4 * 3 * 2 * 1)
#   1 --> 1 (1)
#   9 --> 362880 (9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1)

# Time Complexity: O(N)
# Auxiliary Space Complexity: O(N)

def factorial(n):
    prod = 1
    for i in range(1,n+1):
        prod = prod * i
    return prod

print(factorial(5)) # 120
print(factorial(1)) # 1
print(factorial(9)) # 362880
