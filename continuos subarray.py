from collections import deque

class Solution(object):
    def continuousSubarrays(self, nums):
        n = len(nums)
        left = 0
        result = 0
        max_dq = deque()
        min_dq = deque()

        for right in range(n):
            while max_dq and nums[max_dq[-1]] < nums[right]:
                max_dq.pop()
            max_dq.append(right)

            while min_dq and nums[min_dq[-1]] > nums[right]:
                min_dq.pop()
            min_dq.append(right)

            while nums[max_dq[0]] - nums[min_dq[0]] > 2:
                if max_dq[0] == left:
                    max_dq.popleft()
                if min_dq[0] == left:
                    min_dq.popleft()
                left += 1

            result += (right - left + 1)

        return result
