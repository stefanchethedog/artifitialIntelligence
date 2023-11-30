#!/usr/bin/python3

import queue
import functools

from typing import List, Tuple, Set

priority = queue.PriorityQueue(10)

graph = {
    "A": [(4, "B"), (9, "D")],
    "B": [(4, "A"), (5, "D"), (8, "E"), (7, "F"), (11, "C")],
    "C": [(11, "B"), (3, "F"), (1, "G")],
    "D": [(9, "A"), (5, "B"), (2, "E")],
    "E": [(8, "B"), (2, "D"), (6, "F")],
    "F": [(6, "E"), (7, "B"), (3, "C"), (8, "G")],
    "G": [(1, "C"), (8, "F")],
}


def initializeNodes(graph, start):
    return functools.reduce(
        lambda acc, curr: acc.update(
            {curr: (99999, graph[curr], curr)}
            if start != curr
            else {curr: (0, graph[curr], curr)}
        )
        or acc,
        graph,
        {},
    )


def find_edge(graph, start, end):
    for dete in graph[start]:
        if dete[1] == end:
            return dete[0]


def update_priority_queue(priorityQ, node, newLen):
    ind = list(map(lambda a: a[2], priorityQ.queue)).index(node[1])
    priorityNode = priorityQ.queue[ind]
    if priorityNode[0] > newLen:
        priorityQ.queue.pop(ind)
        priorityQ.put((newLen, priorityNode[1], priorityNode[2]))


# 0 - dist
# 1 - lista grana
# 2 - naziv cvora
def Dixtra(graph, start):
    initialized = initializeNodes(graph, start)
    obidjeni = set()
    dixtra = {}
    priority = queue.PriorityQueue(len(graph))
    priority.put(initialized[start])
    while not priority.empty():
        node = priority.get()
        nodeIsNotVisited = node[2] not in obidjeni

        nodeIsNotVisited and (
            obidjeni.add(node[2]) or dixtra.update({node[2]: node[0:2]})
        )
        for dete in node[1]:
            isNotVisited = dete[1] not in obidjeni
            isNotInQueue = dete[1] not in list(map(lambda a: a[2], priority.queue))
            isNotVisited and not isNotInQueue and update_priority_queue(
                priority,
                dete,
                (node[0] + find_edge(graph, node[2], dete[1])),
            )
            isNotVisited and isNotInQueue and priority.put(
                (
                    node[0] + find_edge(graph, node[2], dete[1]),
                    graph[dete[1]],
                    dete[1],
                )
            )
    return lambda node: dixtra[node]


# DIXTRA CALL
# dix = Dixtra(graph, "A")
# for key in graph:
#    print({key: dix(key)})


def a_star(graph, start, end):
    found_end = False
    open_set = set(start)
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None

    while len(open_set) > 0 and (not found_end):
        node = None
        for next_node in open_set:
            if (
                node is None
                or g[next_node] + graph[next_node][0] < g[node] + graph[node][0]
            ):
                node = next_node

            if node == end:
                found_end = True
                break

            for child, cost in graph[node][1]:  # prolazak kroz dece
                if child not in open_set and child not in closed_set:
                    open_set.add(child)
                    prev_nodes[child] = node
                    g[child] = g[node] + cost
                else:
                    if g[child] > g[node] + cost:
                        g[child] = g[node] + cost
                        prev_nodes[child] = node
                    if child in closed_set:
                        closed_set.remove(child)
                        open_set.add(child)
            open_set.remove(node)
            closed_set.add(node)


# -----------------------------------------------------------------#
def find_lowest_heur(tabla: List[List[int]]) -> Tuple[int, int]:
    row_heur = [15, 15, 15]
    column_heur = [15, 15, 15]

    for i in range(0, 3):
        for j in range(0, 3):
            row_heur[i] -= tabla[i][j]
    for j in range(0, 3):
        for i in range(0, 3):
            column_heur[j] -= tabla[i][j]
    min = (-1, -1)
    min_heur = 2 * 15
    for i in range(0, 3):
        for j in range(0, 3):
            if (
                tabla[i][j] == 0
                and row_heur[i] != 0
                and column_heur[j] != 0
                and row_heur[i] + column_heur[j] < min_heur
            ):
                min = (i, j)
                min_heur = row_heur[i] + column_heur[j]
    return min


def get_possibilities(
    tabla: List[List[int]], node: Tuple[int, int], available_values: Set[int]
) -> List[int]:
    available_vals = sorted(available_values)
    available_vals.reverse()
    returnList = []
    i1 = 0
    i2 = 0
    j1 = 0
    j2 = 0
    if node[0] == 0:
        i1 = 1
        i2 = 2
    elif node[0] == 1:
        i1 = 0
        i2 = 2
    elif node[0] == 2:
        i1 = 0
        i2 = 1

    if node[1] == 0:
        j1 = 1
        j2 = 2
    elif node[1] == 1:
        j1 = 0
        j2 = 2
    elif node[1] == 2:
        j1 = 0
        j2 = 1
    row1 = tabla[node[0]][j1]
    row2 = tabla[node[0]][j2]
    column1 = tabla[i1][node[1]]
    column2 = tabla[i2][node[1]]

    if row2 > row1:
        tmp = row1
        row1 = row2
        row2 = tmp

    if column2 > column1:
        tmp = column1
        column1 = column2
        column2 = tmp

    for possibility in available_vals:
        if row1 + row2 + possibility > 15:
            continue
        if column1 + column2 + possibility > 15:
            continue

        if (
            row2 == 0
            and (15 - row1 - possibility) not in available_values
            and row1 != 0
        ):
            continue
        if (
            column2 == 0
            and (15 - column1 - possibility) not in available_values
            and column1 != 0
        ):
            continue

        returnList.append(possibility)

    return returnList


def resenje_a_star(tabla):
    found_end = False
    open_set = set()
    closed_set = set()

    available_values = set()
    for i in range(1, 10):
        available_values.add(i)
    for i in range(0,3):
        for j in range(0,3):
            if tabla[i][j] != 0:
                available_values.remove(tabla[i][j])
                closed_set.add((i,j))

    start = find_lowest_heur(tabla)

    open_set.add(start)

    prev_nodes = {}
    prev_nodes[start] = None
    last_node = None
    while len(open_set) != 0 and not found_end:
        node = None
        for next_node in open_set:
            node = next_node

        if node == (-1, -1):
            found_end = True
            break
        for possibility in get_possibilities(tabla, node, available_values):
            if possibility in available_values:
                tabla[node[0]][node[1]] = possibility
                prev_nodes[node] = (last_node, possibility)
                available_values.remove(possibility)
                break
        open_set.add(find_lowest_heur(tabla))
        open_set.remove(node)
        closed_set.add(node)
        last_node = node

    path = []
    if found_end:
        while last_node is not None and prev_nodes[last_node] is not None:
            path.append((last_node, prev_nodes[last_node][1]))   
            last_node = prev_nodes[last_node][0]
        path.reverse()
    return path


tabla = [[1, 0, 0], [0, 0, 0], [0, 0, 3]]
i = 0
for korak in resenje_a_star(tabla):
    i+= 1
    print(i, korak)
print('-------------')

for red in tabla:
    print(red)