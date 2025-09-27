class Solution(object):
    def letterCombinations(self, digits):
        if not digits:
            return []
        map = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
        }
        res = []

        def b(i, p):
            if i == len(digits):
                res.append("".join(p))
                return
            for l in map[digits[i]]:
                p.append(l)
                b(i + 1, p)
                p.pop()

        b(0, [])
        return res

