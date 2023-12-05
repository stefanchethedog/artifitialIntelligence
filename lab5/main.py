#!/usr/bin/python3
from typing import List, Dict


def find_len(lista: List) -> int:

    """Count the elements of the lista that are different from '-'"""

    length = 0
    for i in range(0, len(lista)):
        if lista[i] != "-":
            length += 1
    return length


def remove_attacking_squares(
    size: int, copy_row_domains: Dict[int, List], lastAddedRow: int, lastAddedColumn: int
) -> None:
    
    """
    After placing the queen on position: (lastAddedRow, lastAddedColumn), removes the squares that the newly placed queen is attacking\n
    size - size of the board, \n
    copy_row_domains - current domains (available positions in each row), '-' if unavailable
    """

    for i in range(0, lastAddedRow):
        copy_row_domains[i][lastAddedColumn] = "-"
    for i in range(lastAddedRow, size):
        copy_row_domains[i][lastAddedColumn] = "-"

    for j in range(0, lastAddedColumn):
        if j != lastAddedColumn:
            copy_row_domains[lastAddedRow][j] = "-"
    for j in range(lastAddedColumn, size):
        if j != lastAddedColumn:
            copy_row_domains[lastAddedRow][j] = "-"

    i = lastAddedRow - lastAddedColumn
    for j in range(0, size):
        if i >= 0 and i < size:
            if i != lastAddedRow:
                copy_row_domains[i][j] = "-"
        i += 1
    i = lastAddedRow + lastAddedColumn
    for j in range(0, size):
        if i >= 0 and i < size:
            if i != lastAddedRow:
                copy_row_domains[i][j] = "-"
        i -= 1


def find_most_constrained_row(size, copy_row_domains) -> int:

    """Finds the row that has the least available moves"""

    mostConstrainedRow = 0
    for i in range(0, size):
        if find_len(copy_row_domains[i]) == 0:
            continue

        if find_len(copy_row_domains[mostConstrainedRow]) == 0:
            mostConstrainedRow = i
        elif find_len(copy_row_domains[mostConstrainedRow]) > find_len(
            copy_row_domains[i]
        ):
            mostConstrainedRow = i
    return mostConstrainedRow


def csp_solve(n):

    """Uses MVR and Forward checking, together with Backtracking to solve the problem of n queens"""

    rows = {}
    for i in range(0, n):
        rows.update({i: None})
    initialDomain = list()
    for i in range(0, n):
        initialDomain.append(i)

    rowDomains = {}
    for i in range(0, n):
        rowDomains.update({i: initialDomain.copy()})

    paths = []
    for i in range(0, n):
        rows[0] = i
        path = [
            (0, i),
        ]
        csp_solve_recursive(n, rows, rowDomains, 0, paths, path)
    i = 1
    for put in paths:
        if len(put) > 0:
            print(i, put)
            i += 1


def csp_solve_recursive(n, rows, rowDomains, lastAddedRow, paths, path):

    """
    The backtrack part of the algorithm.\n
    Goes into recursion for next available move, checks if there will be any possible moves in the future
    (forward checking).\n
    After realising that there are no further possible moves, checks if we have placed n queens on the board.\n
    If we have, we append the current path into paths, else we append [] to be later pop-ed out
    """

    copy_row_domains = {}
    for key in rowDomains:
        copy_row_domains.update({key: rowDomains[key].copy()})
    lastAddedColumn = rows[lastAddedRow]

    if rowDomains[lastAddedRow][lastAddedColumn] == "-":
        return []

    remove_attacking_squares(n, copy_row_domains, lastAddedRow, lastAddedColumn)
    mostConstrainedRow = find_most_constrained_row(n, copy_row_domains)

    currentPath = path.copy()

    # is this a valid forward checking?
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


csp_solve(8)
