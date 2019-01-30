import sys
import copy
import time


"""update domains of cells in the same square as index"""
def updateSquare(domains, val, index, changedDomainIndexes):
    rowNum = index / 9
    colNum = index % 9
    for j in xrange(3):
        start = 9 * (rowNum - (rowNum % 3) + j) + colNum - colNum % 3
        for k in range(start, start + 3):
            if k != index and val in domains[k]:
                if len(domains[k]) == 1:
                    return False
                domains[k].remove(val)
                changedDomainIndexes.append(k)
    return True


"""update domains of cells in the same column as index"""
def updateColumn(domains, val, index, changedDomainIndexes):
    colNum = index % 9
    for j in xrange(9):
        if j * 9 + colNum != index and val in domains[j * 9 + colNum]:
            if len(domains[j * 9 + colNum]) == 1:
                return False
            domains[j * 9 + colNum].remove(val)
            changedDomainIndexes.append(j * 9 + colNum)
    return True


"""update domains of cells in the same row as index"""
def updateRow(domains, val, index, changedDomainIndexes):
    rowNum = index / 9
    for j in range(9 * rowNum, 9 * (rowNum + 1)):
        if j != index and val in domains[j]:
            if len(domains[j]) == 1:
                return False
            domains[j].remove(val)
            changedDomainIndexes.append(j)
    return True


""" Updates domains of variable's (whose index is index) neighbours in the csp
    in this case, neighbours consist of cells, which are in the same row, column or square
    as the variable with given index  
"""
def updateDomains(domains, val, index, changedDomainIndexes):
    changedDomainIndexes.append(list(domains[index]))
    domains[index] = [val]
    return updateRow(domains, val, index, changedDomainIndexes) \
           and updateColumn(domains, val, index, changedDomainIndexes) \
           and updateSquare(domains, val, index, changedDomainIndexes)


""" Performs backtracking, by returning domains to values they had before filling cell with number index"""
def returnToOldDomains(domains, changedDomainIndexes, val, index):
    domains[index] = list(changedDomainIndexes[0])
    for i in range(1, len(changedDomainIndexes)):
        domains[changedDomainIndexes[i]].append(val)


""" Returns index of the cell which is not yet filled and has minimum remaining values in its domain
    if every cell is filled, returns 81
"""
def mrv(sudoku, domains):
    minn = 10
    minj = 81
    for j in xrange(len(sudoku)):
        if sudoku[j] == '.' and len(domains[j]) < minn:
            minn = len(domains[j])
            minj = j
    return minj


""" Solves given sudoku(list) with given domains for each cell(list of lists) recursively, 
    using forward checking and backtracking by filling the cell with given index. 
    returns True if solved this sudoku, false otherwise
"""
def recursiveSolve(sudoku, domains, index):
    if '.' not in sudoku:
        return True

    for val in domains[index]:
        sudoku[index] = val
        changedDomainIndexes = []
        if not updateDomains(domains, val, index, changedDomainIndexes):
            sudoku[index] = '.'
            returnToOldDomains(domains, changedDomainIndexes, val, index)
            continue
        if recursiveSolve(sudoku, domains, mrv(sudoku, domains)):
            return True
        sudoku[index] = '.'
        returnToOldDomains(domains, changedDomainIndexes, val, index)
    return False


"""solves given sudoku(string) and returns solution as a string, if not solvable, returns "can't solve" """
def solve(sudoku):
    if len(sudoku) < 81:
        return "not a sudoku"
    newLine = "\n"
    sudoku = sudoku[:81]
    domains = [[str(i) for i in range(1, 10)] for j in xrange(81)]
    sudokuList = list(sudoku)
    for i in xrange(81):
        if sudoku[i] != '.':
            updateDomains(domains, sudoku[i], i, [])
    if not recursiveSolve(sudokuList, domains, mrv(sudoku, domains)):
        return "can't solve" + newLine
    return "".join(sudokuList) + newLine


""" Reads sudokus from file specified in arguments, solves them and 
    writes solutions in second file specified in arguments
"""
def main():
    rFile = sys.argv[1]
    wFile = sys.argv[2]
    sudokusFile = open(rFile, "r")
    solutionsFile = open(wFile, "w")
    sudokus = sudokusFile.readlines()
    st = time.time()
    for i in xrange(len(sudokus) - 1):
        solutionsFile.write(solve(sudokus[i]))
    solutionsFile.write(solve(sudokus[-1])[:81])
    print time.time() - st
    sudokusFile.close()
    solutionsFile.close()


if __name__ == "__main__":
    main()
