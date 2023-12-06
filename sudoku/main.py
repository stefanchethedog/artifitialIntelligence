from typing import List
import os


def initialize_domains(size):
    domain = []
    for i in range(0, size):
        domain.append([])
        for j in range(0, size):
            domain[i].append([])
            for k in range(1, 10):
                domain[i][j].append(k)
    return domain


def remove_values_from_domains(domains: List[List], size, i, j, val):
    for l in range(0, size):
        domains[i][j][l] = "-"

    top = i // 3 * 3
    bottom = (i // 3 + 1) * 3
    left = j // 3 * 3
    right = (j // 3 + 1) * 3

    for k in range(0, size):
        if k != j:
            domains[i][k][val - 1] = "-"

        if k != i:
            domains[k][j][val - 1] = "-"

    for k in range(top, bottom):
        for l in range(left, right):
            domains[k][l][val - 1] = "-"


def find_len(niz: List) -> int:
    length = 0
    for i in range(0, len(niz)):
        if niz[i] != "-":
            length += 1
    return length


def find_most_constrained_node(domains: List[List], size: int) -> (int, int):
    most_constrained_len = find_len(domains[0][0])
    most_constrained_indexes = (0, 0)

    for i in range(0, size):
        for j in range(0, size):
            length = find_len(domains[i][j])
            if length == 0:
                continue

            if most_constrained_len == 0:
                most_constrained_indexes = (i, j)
                most_constrained_len = length
                continue

            if most_constrained_len > length:
                most_constrained_indexes = (i, j)
                most_constrained_len = length

    return most_constrained_indexes


def deep_copy_domains(domains, size):
    copy_domain = []
    for i in range(0, size):
        copy_domain.append([])
        for j in range(0, size):
            copy_domain[i].append([])
            copy_domain[i][j] = domains[i][j].copy()
    return copy_domain


def deep_copy_sudoku(sudoku, size):
    copy_sudoku = []
    for i in range(0, size):
        copy_sudoku.append([])
        copy_sudoku[i] = sudoku[i].copy()
    return copy_sudoku


def show_sudoku(sudoku, size):
    sudoku_valid = True
    for i in range(0, size):
        if find_len(sudoku[i]) != 9:
            sudoku_valid = False
            break
    if not sudoku_valid:
        return
    print()
    for k in range(0,9):
        print("===", end="")
    print("===")
    for i in range(0, size):
        for j in range(0, size):
            if j % size == 0:
                print("|", end = "")
            print(" " + str(sudoku[i][j]) + " ", end="")
            if j % 3 == 2:
                print("|", end="")
            if j % size == size - 1:
                print()
        if i % 3 == 2:
            for k in range(0, 9):
                print("===", end="")
            print("===")
    print()
    return sudoku_valid


def solve_sudoku_recursive(sudoku, size, domains, i, j, val):
    domains_copy = deep_copy_domains(domains, size)

    remove_values_from_domains(domains_copy, size, i, j, val)
    sudoku_copy = deep_copy_sudoku(sudoku, size)
    sudoku_copy[i][j] = val

    most_restrained_node = find_most_constrained_node(domains_copy, size)
    i = most_restrained_node[0]
    j = most_restrained_node[1]

    if find_len(domains_copy[i][j]) == 0:
        return show_sudoku(sudoku_copy, size)

    for value in domains_copy[i][j]:
        if value == "-":
            continue
        solve_sudoku_recursive(sudoku_copy, size, domains_copy, i, j, value)

    return False


def solve_sudoku(sudoku, size):
    domains = initialize_domains(size)
    for i in range(0, size):
        for j in range(0, size):
            val = sudoku[i][j]
            if val != "-":
                remove_values_from_domains(domains, size, i, j, val)

    most_restrained_node = find_most_constrained_node(domains, size)
    i = most_restrained_node[0]
    j = most_restrained_node[1]
    for k in range(0, size):
        val = domains[i][j][k]
        if val != "-":
            solve_sudoku_recursive(sudoku, size, domains, i, j, val)


sudoku: List[List] = [
    [8, 2, "-", 5, "-", 1, "-", 7, "-"],
    [7, "-", "-", "-", "-", "-", 4, "-", "-"],
    ["-", "-", "-", "-", "-", 6, "-", "-", "-"],
    ["-", "-", 3, "-", "-", "-", "-", "-", 9],
    ["-", "-", "-", "-", 8, "-", "-", "-", "-"],
    ["-", 1, "-", 2, "-", 7, "-", 4, "-"],
    ["-", "-", "-", "-", 6, "-", "-", 5, "-"],
    ["-", 8, "-", "-", 4, "-", "-", "-", "-"],
    ["-", "-", 1, 8, "-", 5, 3, "-", "-"],
]

k = 0

while k < 81:
    os.system("clear")
    print(k, "Unesite broj ili '-'")
    rows = k // 9 + 1
    columns = k % 9 + 1
    for i in range(0, k):
        print(" " + str(sudoku[i // 9][i % 9]) + " ", end="")
        if i % 3 == 2:
            print("|", end="")
        if i % 9 == 8:
            print()
        if i % 27 == 26:
            for j in range(0, 9):
                print("===", end="")
            print("===")
    ch = input()
    sudoku[k // 9][k % 9] = ch[0] if ch[0] == "-" else int(ch[0])
    k += 1

solve_sudoku(sudoku, 9)
