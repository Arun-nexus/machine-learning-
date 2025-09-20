class Solution(object):
    def lengthOfLongestSubstring(self, s):
        char = set()
        left = 0
        max_len = 0

        for r in range(len(s)):
            while s[r] in char:
                char.remove(s[left])
                left += 1
            char.add(s[r])
            max_len = max(max_len, r - left + 1)

        return max_len
