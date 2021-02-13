import sys

import matrix

def main(argv):
    count = 0
    for line in sys.stdin:
        if count == 0:
            transNumbers = line.split()
            A = matrix.createMatrix(transNumbers)
        if count == 1:
            emissionNumbers = line.split()
            B = matrix.createMatrix(emissionNumbers)
        if count == 2:
            piNumbers = line.split()
            pi = matrix.createMatrix(piNumbers)
        if count == 3: #emissions
            emmNumbers = line.split()
            O = matrix.createVector(emmNumbers)
        count += 1
    T = len(O) # nb of observations
    N = len(A);
    alphaMatrix = [[0.0 for x in range(N)] for y in range(T)]
    t =0
    for i in range(N):
        alphaMatrix[t][i] = B[i][O[t]] * pi[0][i]
    t+=1
    while t<T:
        for i in range(N):
            s = 0
            for j in range(N):
                s+=A[j][i]*alphaMatrix[t-1][j]
            alphaMatrix[t][i] = B[i][O[t]] * s
        t+=1

    result = 0
    for j in range(N):
        result+=alphaMatrix[T-1][j]
    print(result)
    return result


if __name__ == "__main__":
    main(sys.argv)