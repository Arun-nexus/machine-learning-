class Solution(object):
    def firstMissingPositive(self, nums):
        nums = sorted(set(nums))
        j = 1
        for i in range(len(nums)):
            if nums[i] > 0:
                if nums[i] != j:
                    return j
                j += 1
        return j

