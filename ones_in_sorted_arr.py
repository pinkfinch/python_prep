# Challenge 1 : Number of Ones in a Sorted Bit Array
# Given a sorted bit array (values of either 0 or 1), determine the number of 1’s in the array.

# Perform this in O(log(N)) time complexity.

# Input: [0,0,0,1,1,1,1,1,1,1,1]
from numbers import Number

def ones_in_sorted_arr(arr):
    start, finish = 0, len(arr)-1
    while start <= finish and start >=0 and finish <= len(arr)-1:
        mid:Number = round((start+finish)/2)
        if arr[mid] == 1:
            finish = mid-1
        else:
            start = mid+1

    if mid >=0 and mid <= len(arr) - 1 and arr[mid] == 1:
        return len(arr)-mid
    else:
        return 0

print( ones_in_sorted_arr([0,0,0,1,1,1,1,1,1,1,1]))
print( ones_in_sorted_arr([0,0,0,0,0]))
print( ones_in_sorted_arr([1,1,1,1,1,1,1,1]))


