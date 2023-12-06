with open("input.txt") as file:
    entries = [
        [digit.strip().split(" ") for digit in line.split("|")]
        for line in file.readlines()
    ]

    unique_lengths = set((2, 3, 4, 7))
    print(
        sum(len(digit) in unique_lengths for _, output in entries for digit in output)
    )
