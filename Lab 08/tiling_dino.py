# Selinie Wang (jw6qe)
# Collaborators: Jenny Yao
# jw6qe_cs4102_hw8

import networkx
import networkx.algorithms

def tile_image(file_lines):
    # print(file_lines)

    counter = 0
    g = networkx.DiGraph()
    e = networkx.DiGraph()
    black = []
    red = []
    coor = []

    w, h = len(file_lines), len(file_lines[0])
    values = [[0 for j in range(h-1)] for i in range(w)]

    for col in range(0, len(file_lines)):
        for row in range(0, len(file_lines[0])-1):
            if file_lines[col][row] == "#":
                values[col][row] = 1
                counter = counter + 1
                coor.append(str(row) + ", " + str(col))

                # split evens and odds into two arrays
                if (col+row) % 2 == 0:
                    black.append((row, col))
                else:
                    red.append((row, col))
            else:
                values[col][row] = 0

    # create bipartite graph with evens and odds
    g.add_nodes_from(black, bipartite = 0)
    g.add_nodes_from(red, bipartite = 1)

    # create source and sink nodes
    g.add_node("source")
    for edge in range(0, len(black)):
        g.add_edge("source", black[edge], capacity = 1)

    g.add_node("sink")
    for edge in range(0, len(red)):
        g.add_edge(red[edge], "sink", capacity = 1)

    # create edges to the nodes
    for col in range(0, len(file_lines)):
        for row in range(0, len(file_lines[0])-1):
            if file_lines[col][row] == "#":
                if (col + 1) < len(file_lines):
                    if (col+row) % 2 == 0:
                        if file_lines[col+1][row] == "#":
                            g.add_edge((row, col), (row, col+1), capacity = 1)
                            # g.add_edge(str(row) + ", " + str(col), str(row) + ", " + str(col+1))
                if (row + 1) < len(file_lines[0]):
                    if (col+row) % 2 == 0:
                        if file_lines[col][row+1] == "#":
                            g.add_edge((row, col), (row+1, col), capacity = 1)
                            # g.add_edge(str(row) + ", " + str(col), str(row+1) + ", " + str(col))
                if (col - 1) >= 0:
                    if (col + row) % 2 == 0:
                        if file_lines[col-1][row] == "#":
                            g.add_edge((row, col), (row, col-1), capacity = 1)
                            # g.add_edge(str(row) + ", " + str(col), str(row) + ", " + str(col-1))
                if (row - 1) >= 0:
                    if (col + row) % 2 == 0:
                        if file_lines[col][row-1] == "#":
                            g.add_edge((row, col), (row-1, col), capacity = 1)
                            # g.add_edge(str(row) + " " + str(col), str(row-1) + ", " + str(col))


    # print("Nodes: ", g.nodes) # split by bipartite graph
    # print("Edges: ", g.edges) # print out the edges of graph
    networkx.maximum_flow(g, "source", "sink")
    # print(networkx.maximum_flow(g, "source", "sink"))

    flow, dict = networkx.maximum_flow(g, "source", "sink")
    dictionary1 = dict
    for k, v in dictionary1.items():
        for k1, v1 in v.items():
            if v1 == 1:
                if k != "source" and k1 != "sink":
                    print(k[0], k[1], k1[0], k1[1])

    # nodes minus source and sink
    if flow == ((len(g.nodes)-2)/2):
        return("")
    elif counter % 2 != 0:
        return["impossible"]
    elif len(black) != len(red):
        return["impossible"]
    else:
        return["impossible"]