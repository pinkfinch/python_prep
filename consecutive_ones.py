from typing import List

class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        l = 0
        max_ones = 0
        zero_count = 0

        for r in range(len(nums)):
            # Expand window
            if nums[r] == 0:
                zero_count += 1

            # Shrink window if we have more than 1 zero
            while zero_count > 1:
                if nums[l] == 0:
                    zero_count -= 1
                l += 1

            # Update max length
            max_ones = max(max_ones, r - l + 1)

        return max_ones

s = Solution()
print(s.findMaxConsecutiveOnes([0]))