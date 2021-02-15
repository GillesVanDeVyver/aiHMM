from sys import stdin
import matrix


def main():
    A = matrix.create_matrix(stdin.readline().split())
    B = matrix.create_matrix(stdin.readline().split())
    pi = matrix.create_matrix(stdin.readline().split())
    emissions = matrix.create_vector(stdin.readline().split())
    T = len(emissions)  # nb of observations
    N = len(A)
    delta_matrix = [[0.0 for _ in range(N)] for _ in range(T)]
    # remember that delta_id_matrix always have the index written as actual index - 2 (instead of -1)
    # since t = 1 has no predecessor
    delta_id_matrix = [[0 for _ in range(N)] for _ in range(T-1)]

    for i in range(N):
        delta_matrix[0][i] = B[i][emissions[0]] * pi[0][i]
    for t in range(1, T):
        for i in range(N):
            temp = []
            for j in range(N):
                temp.append(A[j][i] * delta_matrix[t-1][j] * B[i][emissions[t]])
            delta_matrix[t][i] = max(temp)
            delta_id_matrix[t-1][i] = temp.index(delta_matrix[t][i])

    seq = [delta_matrix[T-1].index(max(delta_matrix[T-1]))]
    for t in reversed(range(T-1)):
        seq.append(delta_id_matrix[t][seq[-1]])
    seq = reversed(seq)
    result = ""
    for state in seq:
        result += str(state) + " "
    print(result[:-1])
    return result[:-1]


if __name__ == "__main__":
    main()
