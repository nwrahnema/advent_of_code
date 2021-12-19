from collections import Counter

with open("input.txt") as file:
    columns = zip(*file.readlines())
    gamma_rate = "".join(max(["0", "1"], key=bits.count) for bits in columns)
    epsilon_rate = "".join("0" if bit == "1" else "1" for bit in gamma_rate)

    print(int(gamma_rate, base=2) * int(epsilon_rate, base=2))
