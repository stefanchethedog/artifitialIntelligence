#!/usr/bin/python3
import queue

graph = {
    "node1": ["node5", "node2"],
    "node2": ["node4"],
    "node3": ["node2"],
    "node4": ["node5"],
    "node5": ["node1"],
}


def obrada(node):
    print(node)


def breadth_first_search(graph, start, end):
    obidjeni = {}
    zaObilazak = queue.Queue(len(graph))
    zaObilazak.put(start)

    while not zaObilazak.empty():
        cvor = zaObilazak.get()
        obidjeni.get(cvor, None) == None and obidjeni.update({cvor: "1"})
        obrada(cvor)
        if cvor == end:
            return
        for dete in graph[cvor]:
            obidjeni.get(dete, None) == None and zaObilazak.put(dete)


def depth_first_search(graph, start, end):
    obidjeni = {}
    zaObilazak = queue.LifoQueue(len(graph))
    zaObilazak.put(start)

    while not zaObilazak.empty():
        cvor = zaObilazak.get()
        obidjeni.get(cvor, None) == None and obidjeni.update({cvor: "1"})
        obrada(cvor)
        if cvor == end:
            return
        for dete in graph[cvor]:
            obidjeni.get(dete, None) == None and zaObilazak.put(dete)


depth_first_search(graph, "node1", "node5")
# breadth_first_search(graph, 'node1', 'node5')



    