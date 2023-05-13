from collections import defaultdict

# 그래프 생성
graph = defaultdict(set)
vertices = set()

with open("dict_simplified.txt", "r", encoding="utf-8") as f:
    for line in f:
        word, desc = line.strip().split("\t")
        vertices.add(word)
        for v in vertices:
            if v in desc.split():
                graph[word].add(v)
                graph[v].add(word)

# 문제 1: 정점의 개수와 에지의 개수 출력
num_vertices = len(vertices)
num_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
print(f"Answer1: {num_vertices} {num_edges}")

# 문제 2: 차수가 최대인 정점 출력
max_degree = -1
max_degree_word = ""
for word, neighbors in graph.items():
    degree = len(neighbors)
    if degree > max_degree:
        max_degree = degree
        max_degree_word = word
print(f"Answer2: {max_degree_word} {max_degree}")

# 문제 3: 가장 큰 연결요소의 크기 출력
visited = set()
max_component_size = 0
for word in vertices:
    if word not in visited:
        component_size = 0
        stack = [word]
        while stack:
            current_word = stack.pop()
            if current_word not in visited:
                visited.add(current_word)
                component_size += 1
                stack.extend(graph[current_word])
        if component_size > max_component_size:
            max_component_size = component_size
print(f"Answer3: {max_component_size}")

# 문제 4: 단어 x로부터 거리가 k 이하인 모든 단어 출력
def bfs(start_word, k):
    visited = set()
    queue = [(start_word, 0)]
    while queue:
        current_word, distance = queue.pop(0)
        if current_word not in visited:
            visited.add(current_word)
            if distance <= k:
                print(current_word)
                queue.extend((neighbor, distance+1) for neighbor in graph[current_word] if neighbor not in visited)
    return len(visited)

word = "mountain"
k = 2
print(f"Answer4: ({word}와 정수 {k}를 입력했을 시)")
num_words = bfs(word, k)
print(num_words)
