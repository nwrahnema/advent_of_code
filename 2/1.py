position = 0
depth = 0

with open("input.txt") as file:
    for instruction in file.readlines():
        direction, distance = instruction.split(' ')
        distance = int(distance)
        match direction:
            case "forward":
                position += distance
            case "down":
                depth += distance
            case "up":
                depth -= distance
                
print(position * depth)
