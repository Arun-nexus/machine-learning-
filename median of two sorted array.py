class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        nums3 = nums1 + nums2
        nums3.sort()
        size = len(nums3)

        if size % 2 == 1:
            return nums3[size // 2]
        else:
            mid1 = nums3[size // 2 - 1]
            mid2 = nums3[size // 2]
            return (mid1 + mid2) / 2.0


