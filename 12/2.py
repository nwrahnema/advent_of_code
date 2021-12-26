from collections import defaultdict


START = "start"
END = "end"

with open("input.txt") as file:
    connected = [line.split("-") for line in file.read().splitlines()]
    graph = defaultdict(list)
    for cave1, cave2 in connected:
        graph[cave1].append(cave2)
        graph[cave2].append(cave1)

    visited = defaultdict(int)

    def dfs(cur: str, free_space: bool) -> int:
        if cur == END:
            return 1

        if visited[cur] == 1:
            if free_space and cur != START:
                free_space = False
            else:
                return 0
        elif visited[cur] > 1:
            return 0

        is_small_cave = all(letter.islower() for letter in cur)
        if is_small_cave:
            visited[cur] += 1
        num_paths = sum(dfs(nxt, free_space) for nxt in graph[cur])
        if is_small_cave:
            visited[cur] -= 1

        return num_paths

    print(dfs(START, True))
