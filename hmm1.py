from sys import stdin
import matrix


def main():
    A = matrix.create_matrix(stdin.readline().split())
    B = matrix.create_matrix(stdin.readline().split())
    pi = matrix.create_matrix(stdin.readline().split())
    emissions = matrix.create_vector(stdin.readline().split())
    T = len(emissions)  # nb of observations
    N = len(A)
    alpha_matrix = [[0.0 for _ in range(N)] for _ in range(T)]
    for i in range(N):
        alpha_matrix[0][i] = B[i][emissions[0]] * pi[0][i]
    for t in range(1, T):
        for i in range(N):
            s = 0
            for j in range(N):
                s += A[j][i] * alpha_matrix[t-1][j]
            alpha_matrix[t][i] = B[i][emissions[t]] * s

    result = 0
    for i in range(N):
        result += alpha_matrix[T-1][i]
    print(result)
    return result


if __name__ == "__main__":
    main()
