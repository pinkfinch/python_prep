# Given a sorted array of unique integers, and a target value determine the index of
# a matching value within the array. If there is not match, return -1.
# Input: [1,3,4,5,6,7,8,10,11,13,15,17,20,22], 17
# Output: 11

from numbers import Number


# def binary_search(arr, value):
#     if arr is None or len(arr) == 0:
#         return -1
#     start,finish = 0, len(arr)-1
#     while start <= finish and start >= 0 and finish < len(arr):
#         mid: Number = round((start + finish)/2)
#         print( "mid is ", mid)
#         if arr[mid] == value:
#             return mid
#         elif arr[mid] > value:
#             finish = mid-1
#         else:
#             start = mid+1
#     return -1

def binary_search(arr, value):
    start,finish = 0, len(arr)-1

    while start < finish:
        mid = (start + finish) // 2
        if value <= arr[mid]:
            finish = mid
        else:
            start = mid+1
    return finish if value == arr[finish] else -1





print( binary_search([1,3,4,5,6,7,8,10,11,13,15,17,20,22], 17)) #return 11
print( binary_search([1,3,4,5,6,7,8,10,11,13,15,17,20,22], 12)) # return -1
print( binary_search([1,3,4,5,6,7,8,10,11,13,15,17,20,22], -1))  # return -1
print( binary_search([1,3,4,5,6,7,8,10,11,13,15,17,20,22], 25))  # return -1

