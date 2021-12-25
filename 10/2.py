with open("input.txt") as file:
    lines = file.read().splitlines()

    brace_pairs = {"(": ")", "{": "}", "[": "]", "<": ">"}
    brace_scores = {")": 1, "]": 2, "}": 3, ">": 4}

    scores = []
    for line in lines:
        stack = []
        for brace in line:
            if brace in brace_pairs.keys():
                stack.append(brace)
            elif brace in brace_pairs.values():
                if brace_pairs[stack[-1]] == brace:
                    stack.pop()
                else:
                    break
            else:
                raise Exception(f"Unexpected character: '{brace}'")
        else:
            completion_string = reversed([brace_pairs[brace] for brace in stack])
            score = 0
            for brace in completion_string:
                score *= 5
                score += brace_scores[brace]
            scores.append(score)

    scores.sort()
    print(scores[len(scores) // 2])
