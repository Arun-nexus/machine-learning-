class Solution(object):
    def solveSudoku(self, board):
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empties = []

        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    empties.append((i, j))
                else:
                    num = board[i][j]
                    rows[i].add(num)
                    cols[j].add(num)
                    boxes[(i // 3) * 3 + j // 3].add(num)

        def backtrack(k=0):
            if k == len(empties):
                return True

            i, j = empties[k]
            b = (i // 3) * 3 + j // 3

            for ch in '123456789':
                if ch not in rows[i] and ch not in cols[j] and ch not in boxes[b]:
                    board[i][j] = ch
                    rows[i].add(ch)
                    cols[j].add(ch)
                    boxes[b].add(ch)

                    if backtrack(k + 1):
                        return True

                    board[i][j] = '.'
                    rows[i].remove(ch)
                    cols[j].remove(ch)
                    boxes[b].remove(ch)

            return False

        backtrack()
