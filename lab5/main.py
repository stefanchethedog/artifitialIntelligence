#!/usr/bin/python3
from typing import List, Dict
from sys import argv


def find_len(lista: List) -> int:
    """Count the elements of the lista that are different from '-'"""

    length = 0
    for i in range(0, len(lista)):
        if lista[i] != "-":
            length += 1
    return length


def remove_attacking_squares(
    size: int,
    copy_row_domains: Dict[int, List],
    lastAddedRow: int,
    lastAddedColumn: int,
) -> None:
    """
    After placing the queen on position: (lastAddedRow, lastAddedColumn), removes the squares that the newly placed queen is attacking\n
    size - size of the board, \n
    copy_row_domains - current domains (available positions in each row), '-' if unavailable
    """
    i1 = lastAddedRow - lastAddedColumn
    i2 = lastAddedRow + lastAddedColumn

    for i in range(0, size):
        copy_row_domains[i][lastAddedColumn] = "-"  # column '-'

        if i != lastAddedColumn:
            copy_row_domains[lastAddedRow][i] = "-"  # row '-'

        if i1 >= 0 and i1 < size:
            if i1 != lastAddedRow:
                copy_row_domains[i1][i] = "-"
        i1 += 1

        if i2 >= 0 and i2 < size:
            if i2 != lastAddedRow:
                copy_row_domains[i2][i] = "-"
        i2 -= 1


def find_most_constrained_row(size, copy_row_domains) -> int:

    """Finds the row that has the least available moves"""

    mostConstrainedRow = 0
    mostConstrainedLength = find_len(copy_row_domains)

    for i in range(0, size):
        length = find_len(copy_row_domains[i])
        if length == 0:
            continue

        if mostConstrainedLength == 0:
            mostConstrainedRow = i
            mostConstrainedLength = length
            continue

        if length < mostConstrainedLength:
            mostConstrainedRow = i
            mostConstrainedLength = length

    return mostConstrainedRow

def initialize_domains(n):
    rowDomains = {}
    for i in range(0, n):
        rowDomains.update({i: []})
        for j in range(0,n):
            rowDomains[i].append(j)
    return rowDomains

def deep_copy_domains(rowDomains):
    copy_row_domains = {}
    for key in rowDomains:
        copy_row_domains.update({key: rowDomains[key].copy()})
    return copy_row_domains
   

def csp_solve_recursive(n, rows, rowDomains, lastAddedRow, paths, path):
    """
    The backtrack part of the algorithm.\n
    Goes into recursion for next available move, checks if there will be any possible moves in the future
    (forward checking).\n
    After realising that there are no further possible moves, checks if we have placed n queens on the board.\n
    If we have, we append the current path into paths, else we append [] to be later pop-ed out
    """

    copy_row_domains = deep_copy_domains(rowDomains)
    
    lastAddedColumn = rows[lastAddedRow]

    if rowDomains[lastAddedRow][lastAddedColumn] == "-":
        return []

    remove_attacking_squares(n, copy_row_domains, lastAddedRow, lastAddedColumn)
    mostConstrainedRow = find_most_constrained_row(n, copy_row_domains)

    currentPath = path.copy()

    # is this a valid forward checking method?
    if find_len(copy_row_domains[mostConstrainedRow]) == 0:
        return [] if len(currentPath) < n else currentPath

    for column in copy_row_domains[mostConstrainedRow]:
        if column == "-":
            continue

        rows[mostConstrainedRow] = column
        currentPath.append((mostConstrainedRow, column))
        val = csp_solve_recursive(
            n, rows, copy_row_domains, mostConstrainedRow, paths, currentPath
        )
        if val != None and len(val) == n:
            paths.append(val)
        if len(paths) > 0 and len(paths[-1]) == 0:
            paths.pop()
        currentPath.pop()

def csp_solve(n):
    
    """Uses MVR and Forward checking, together with Backtracking to solve the problem of n queens"""

    rows = {}
    for i in range(0, n):
        rows.update({i: None})
    
    rowDomains = initialize_domains(n)
    
    paths = []
    for i in range(0, n):
        rows[0] = i
        path = [(0, i)]
        csp_solve_recursive(n, rows, rowDomains, 0, paths, path)

    i = 1
    for put in paths:
        if len(put) > 0:
            print(i, put)
            i += 1



if len(argv) > 1:
    n = int(argv[1]) or 8

csp_solve(n)
