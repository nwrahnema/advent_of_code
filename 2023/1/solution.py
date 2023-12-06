from pathlib import Path

with open(Path(__file__).with_name("input.txt")) as f:
    lines = f.read().splitlines()

num_map = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}

converted: list[list[str]] = []
for i in range(len(lines)):
    result: list[str] = []
    tmp = lines[i]
    while tmp:
        if tmp[0].isdigit():
            result.append(tmp[0])
            tmp = tmp[1:]
        else:
            for num, str_num in num_map.items():
                if tmp.startswith(str_num):
                    result.append(str(num))
                    tmp = tmp[len(str_num) - 1 :]
                    break
            else:
                tmp = tmp[1:]
    converted.append(result)

print(converted)
filtered = [[c for c in line if c.isdigit()] for line in converted]
print(sum(int(line[0] + line[-1]) for line in filtered))
