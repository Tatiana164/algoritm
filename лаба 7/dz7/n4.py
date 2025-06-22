from pprint import pprint

def solve_n_queens_one(N: int):
    # cols — занятые столбцы
    # diag1 — занятые диагонали i+j
    # diag2 — занятые диагонали i-j
    cols = set()
    diag1 = set()
    diag2 = set()
    board = [["."] * N for _ in range(N)]
    solution = []

    def backtrack(row: int) -> bool:
        if row == N:
            for r in board:
                solution.append("".join(r))
            return True

        for c in range(N):
            if c in cols or (row + c) in diag1 or (row - c) in diag2:
                continue
            cols.add(c)
            diag1.add(row + c)
            diag2.add(row - c)
            board[row][c] = "Q"

            if backtrack(row + 1):
                return True

            cols.remove(c)
            diag1.remove(row + c)
            diag2.remove(row - c)
            board[row][c] = "."

        return False

    backtrack(0)
    return solution

if __name__ == "__main__":
    N = int(input().strip())
    sol = solve_n_queens_one(N)
    pprint(sol)
