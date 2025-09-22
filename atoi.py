class Solution(object):
    def myAtoi(self, s):
        s = s.strip()
        if not s:
            return 0

        res = []
        i = 0
        if s[0] in ['-', '+']:
            res.append(s[0])
            i += 1
        while i < len(s) and s[i].isdigit():
            res.append(s[i])
            i += 1

        if len(res) == 0 or (len(res) == 1 and res[0] in ['-', '+']):
            return 0

        res = int("".join(res))
        INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1
        if res < INT_MIN: return INT_MIN
        if res > INT_MAX: return INT_MAX

        return res
