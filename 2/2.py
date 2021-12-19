aim = 0
position = 0
depth = 0

with open("input.txt") as file:
    for instruction in file.readlines():
        direction, amount = instruction.split(' ')
        amount = int(amount)
        match direction:
            case "forward":
                position += amount
                depth += aim * amount
            case "down":
                aim += amount
            case "up":
                aim -= amount
                
print(position * depth)
