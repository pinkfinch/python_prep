# Challenge 1 : Sorted Two Sum
# Given a sorted array of integers and a target value, determine if there exists two integers in the array that sum up to the target value.

# See if you can solve this in O(N) time and O(1) auxiliary space.
def sorted_two_sum(arr, target):
    if(len(arr) <= 1 or target is None):
        return False
    left, right = 0, len(arr) - 1
    while(left < right):
        if(arr[left] + arr[right] == target):
            return True
        elif(arr[left] + arr[right] < target):
            left += 1
        else:
            right -= 1

    return False


print(sorted_two_sum([1,3,7,9,10,12,13,14,15], 12))
print(sorted_two_sum([1,3,7,9,10,12,13,14,15], 15))
print(sorted_two_sum([1,3,7,9,10,12,13,14,15], 0))
