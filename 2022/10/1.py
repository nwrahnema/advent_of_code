with open("input.txt") as file:
    lines = file.read().splitlines()

    brace_pairs = {"(": ")", "{": "}", "[": "]", "<": ">"}
    brace_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

    total = 0
    for line in lines:
        stack = []
        for brace in line:
            if brace in brace_pairs.keys():
                stack.append(brace)
            elif brace in brace_pairs.values():
                if brace_pairs[stack[-1]] == brace:
                    stack.pop()
                else:
                    total += brace_scores[brace]
                    break
            else:
                raise Exception(f"Unexpected character: '{brace}'")
    print(total)
