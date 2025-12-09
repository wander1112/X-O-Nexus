class Vertex:
    def __init__(self, val, position):
        self.val = val
        self.position = position

    def __repr__(self):
        return f"V({self.val})"


class Edge:
    def __init__(self, value, origin, dest):
        self.value = value
        self.origin = origin   # Vertex object
        self.dest = dest       # Vertex object

    def __repr__(self):
        return f"E({self.origin.val}-{self.value}->{self.dest.val})"


class Graph:
    def __init__(self):
        self.vertices = []
        self.edgeList = []     # list of Edge objects
        self.numEdges = 0
        self.numVertices = 0

    def addVertex(self, val):
        v = Vertex(val, self.numVertices)
        self.vertices.append(v)
        self.numVertices += 1
        return v

    def addEdge(self, val, origin, dest):
        e = Edge(val, origin, dest)
        self.edgeList.append(e)
        self.numEdges += 1
        return e

    def removeEdge(self, edge):
        if edge in self.edgeList:
            self.edgeList.remove(edge)
            self.numEdges -= 1
            return True
        return False

    def removeVertex(self, vertex):
        # Remove all edges touching this vertex
        for e in self.edgeList[:]:     # copy list to remove safely
            if e.origin is vertex or e.dest is vertex:
                self.edgeList.remove(e)
                self.numEdges -= 1

        # Remove vertex
        pos = vertex.position
        self.vertices.pop(pos)
        self.numVertices -= 1

        # Update vertex positions
        for i in range(pos, len(self.vertices)):
            self.vertices[i].position = i

    def display(self):
        for e in self.vertices:
            print(e.val)

    def bfs_edgelist(graph, start_vertex):
        visited = {}
        order = []
        q = [start_vertex]
        head = 0

        while head < len(q):
            v = q[head]
            head += 1
            if not (v in visited):
                visited[v] = True
                order.append(v.val)
                i = 0
                while i < len(graph.edgeList):
                    e = graph.edgeList[i]
                    if e.origin is v:
                        if not (e.dest in visited):
                            q.append(e.dest)
                    i += 1

        print("BFS Traversal:", order)
        return order


    def dfs_edgelist(graph, start_vertex):
        visited = {}
        order = []
        stack = [start_vertex]

        while stack:
            v = stack.pop()
            if not (v in visited):
                visited[v] = True
                order.append(v.val)
                i = len(graph.edgeList) - 1
                while i >= 0:
                    e = graph.edgeList[i]
                    if e.origin is v:
                        if not (e.dest in visited):
                            stack.append(e.dest)
                    i -= 1

        print("DFS Traversal:", order)
        return order



g = Graph()
v1 = g.addVertex(1)
v2 = g.addVertex(2)
v3 = g.addVertex(3)
v4 = g.addVertex(4)
v5 = g.addVertex(5)
'''
g.addEdge('a', v1, v2)
g.addEdge('c', v5, v3)
g.addEdge('d', v2, v4)
g.addEdge('e', v1, v3)

g.display()

print("\nRemoving vertex 2...")
g.removeVertex(v2)

g.bfs_edgelist(v1)
g.dfs_edgelist(v1)

'''
g.display()
