from itertools import chain


def isBoardWin(board: list[list[str]]) -> bool:
    rows = board
    cols = zip(*board)

    return any(all(num == "" for num in line) for line in chain(rows, cols))


def setNumberDrawn(board: list[list[str]], num: str) -> None:
    for row in board:
        for i in range(len(row)):
            if row[i] == num:
                row[i] = ""
                return


def calculateScore(board: list[list[str]]) -> int:
    return sum(int(num) if num != "" else 0 for row in board for num in row)


with open("input.txt") as file:
    nums = file.readline().split(",")
    boards = [
        [row.split() for row in board.split("\n")]
        for board in file.read().strip().split("\n\n")
    ]

    for num in nums:
        for board in boards:
            setNumberDrawn(board, num)
            if isBoardWin(board):
                print(calculateScore(board) * int(num))
                exit()
