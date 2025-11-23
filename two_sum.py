# Example 1: Two Sum
# Given an array of integers, and a target value determine if there are two integers that add to the sum.

# Input: [4,2,6,5,7,9,10], 13

# Output: true


def two_sum(arr, target):
    current_set = set()
    for num in arr:
        if num in current_set:
            return True
        else:
            difference = target-num
            current_set.add(difference)
    return False

print(two_sum([4,2,6,5,7,9,10], 13))
print(two_sum([4,2,6,5,7,9,10], 22))
print(two_sum([4,2,6,5,7,9,10], -13))
