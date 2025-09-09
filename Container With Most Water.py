class Solution(object):
    def maxArea(self, height):
        left, right = 0, len(height) - 1
        volume = 0

        while left < right:
            if volume < (right - left) * min(height[left], height[right]):
                volume = (right - left) * min(height[left], height[right])
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return volume
