from collections import defaultdict


START = "start"
END = "end"

with open("input.txt") as file:
    connected = [line.split("-") for line in file.read().splitlines()]
    graph = defaultdict(list)
    for cave1, cave2 in connected:
        graph[cave1].append(cave2)
        graph[cave2].append(cave1)

    visited = set()

    def dfs(cur: str) -> int:
        if cur in visited:
            return 0

        if cur == END:
            return 1

        if all(letter.islower() for letter in cur):
            visited.add(cur)

        num_paths = sum(dfs(nxt) for nxt in graph[cur])
        visited.discard(cur)

        return num_paths

    print(dfs(START))
