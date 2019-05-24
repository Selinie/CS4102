# Selinie Wang (jw6qe)
# Collaborators: Jenny Yao
# jw6qe_cs4102_hw8b

class MaxFlow:
    def __init__(self, graph):
        # residual graph
        self.graph = graph
        self.black = len(graph)
        self.red = len(graph[0])
        return

    def maxflow(self, u, match, visited):
        for node in range(self.red):
            if self.graph[u][node]:
                if visited[node] == False:
                    visited[node] = True
                    if match[node] == -1 or self.maxflow(match[node], match, visited):
                        match[node] = u
                        return True
        return False

    def numMax(self):
        match = [-1] * self.red
        result = 0
        for i in range(self.black):
            visited = [False] * self.red
            if self.maxflow(i, match, visited):
                result = result + 1
        return result