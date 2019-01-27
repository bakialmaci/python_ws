import collections
import math

nodes = [
        [1,[0,0,1],[2,2]], #[{node:(x,y,verify)},{connected_nodes0:distance_from_connected_nodes0},{...]
        [2,[0,2,1],[3,1],[4,1]],
        [3,[1,2,1],[5,1],[6,1]],
        [5,[1,1,0],[3,1]],
        [6,[0,1,0],[3,1]],
        [4,[0,3,0],[2,1]]
        ]

# print(nodes[0][0])  # sözlük kullanmaya gerek yok ozamaan hepsini arraylerin içerisinde düzgün tutalım.

class Graph:
  def __init__(self):
    self.vertices = set()
    # makes the default value for all vertices an empty list
    self.edges = collections.defaultdict(list)
    self.weights = {}
  def add_vertex(self, value):
    self.vertices.add(value)
  def add_edge(self, from_vertex, to_vertex, distance):
    if from_vertex == to_vertex: pass  # no cycles allowed
    self.edges[from_vertex].append(to_vertex)
    self.weights[(from_vertex, to_vertex)] = distance

def dijkstra(graph, start):
  # initializations
  S = set()
  # delta represents the length shortest distance paths from start -> v, for v in delta.
  # We initialize it so that every vertex has a path of infinity
  delta = dict.fromkeys(list(graph.vertices), math.inf)
  previous = dict.fromkeys(list(graph.vertices), None)
  # then we set the path length of the start vertex to 0
  delta[start] = 0
  # while there exists a vertex v not in S
  while S != graph.vertices:
    # let v be the closest vertex that has not been visited...it will begin at 'start'
    v = min((set(delta.keys()) - S), key=delta.get)
    # for each neighbor of v not in S
    for neighbor in set(graph.edges[v]) - S:
      new_path = delta[v] + graph.weights[v,neighbor]
      # is the new path from neighbor through
      if new_path < delta[neighbor]:
        # since it's optimal, update the shortest path for neighbor
        delta[neighbor] = new_path
        # set the previous vertex of neighbor to v
        previous[neighbor] = v
    S.add(v)
  return (delta, previous)

def shortest_path(graph, start, end):
  delta, previous = dijkstra(graph, start)

  path = []
  vertex = end

  while vertex is not None:
    path.append(vertex)
    vertex = previous[vertex]

  path.reverse()
  return path

G = Graph()

def add_node(n):
    G.add_vertex(nodes[n][0])

def add_edge(n1,n2):
    G.add_edge(nodes[find_array_location(n1)[0]][0], nodes[find_array_location(n2)[0]][0], nodes[0][2][1])

def find_location(x):
    try:
        for i in range(len(nodes)):
            if nodes[i][0]==x:
              return nodes[i][1][0],nodes[i][1][1]
              break
    except:
        pass

def find_array_location(x):
    try:
        for i in range(len(nodes)):
            if nodes[i][0]==x:
              return i,0
              break
    except:
        pass

def find_distance(n1,n2,l):
    try:
        for i in range(len(nodes)):
            if nodes[i][0]==x:
              return i,0
              break
    except:
        pass

add_node(0)
add_node(1)
add_node(2)
add_node(3)
add_node(4)
add_node(5)

add_edge()

#________________a__n_________a__c__n_________a__c__l__
G.add_edge(nodes[0][0], nodes[0][2][0], nodes[0][2][1])
G.add_edge(nodes[1][0], nodes[1][2][0], nodes[1][2][1])
G.add_edge(nodes[1][0], nodes[1][3][0], nodes[1][3][1])
G.add_edge(nodes[2][0], nodes[2][2][0], nodes[2][2][1])
G.add_edge(nodes[2][0], nodes[2][3][0], nodes[2][3][1])
G.add_edge(nodes[3][0], nodes[3][2][0], nodes[3][2][1])
G.add_edge(nodes[4][0], nodes[4][2][0], nodes[4][2][1])
G.add_edge(nodes[5][0], nodes[5][2][0], nodes[5][2][1])

print("Shortest Path::",shortest_path(G, 1, 5))
l = len(shortest_path(G,1,5))
print("Target Coordinates::",find_location(shortest_path(G, 1, 5)[l-1]))
