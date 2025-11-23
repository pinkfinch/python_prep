#Given a bit array, return it sorted in-place (a bit array is simply an array that contains only bits, either a 1 or a 0).
#See if you can solve this in O(N) time and O(1) auxiliary space.

def sorted_bit_array(arr):
    start = 0
    ending = len(arr)-1

    while (start < ending):
        while(arr[start] == 0 and start < ending):
            start += 1
        while(arr[ending] == 1 and start < ending):
            ending -= 1
        arr[start], arr[ending] = arr[ending], arr[start]

    return arr



sorted_array = sorted_bit_array([1, 1, 1, 1, 0, 0, 0, 1, 0, 1])
print(sorted_array)
