import sys


def createMatrix(line):
    nbRows = int(line[0])
    nbCols = int(line[1])
    result = [[0.0 for x in range(nbCols)] for y in range(nbRows)]
    k = 2
    for i in range(0, nbRows):
        for j in range(0, nbCols):
            result[i][j] = float(line[k])
            k += 1
    return result


# vec is 1xm vector
# matrix is mxn matrix
def matrixVecMul(vec, matrix):
    m = len(matrix)
    n = len(matrix[0])
    result = [[0.0 for x in range(n)]]
    for i in range(0, n):
        for j in range(0, m):
            result[0][i] += vec[0][j] * matrix[j][i]
    for i in range(0, n):
        result[0][i] = round(result[0][i],10)

    return result


def main(argv):
    count = 0
    for line in sys.stdin:
        if count ==0:
            transNumbers = line.split()
            A = createMatrix(transNumbers)
        if count ==1:
            emissionNumbers = line.split()
            B = createMatrix(emissionNumbers)
        if count == 2:
            piNumbers = line.split()
            pi = createMatrix(piNumbers)
        count+=1
    v1 = matrixVecMul(pi, A)
    v2 = matrixVecMul(v1, B)
    n = len(v2[0])
    result = "1 " + str(n)
    for i in range(0, n):
        result+= " " + str(v2[0][i])
    print(result)
    return result

if __name__ == "__main__":
    main(sys.argv)