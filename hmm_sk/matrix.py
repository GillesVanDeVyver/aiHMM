def create_matrix(line):
    nb_rows = int(line[0])
    nb_cols = int(line[1])
    result = [[0.0 for _ in range(nb_cols)] for _ in range(nb_rows)]
    k = 2
    for i in range(0, nb_rows):
        for j in range(0, nb_cols):
            result[i][j] = float(line[k])
            k += 1
    return result


def create_vector(line):
    nb_rows = int(line[0])
    result = [0 for _ in range(nb_rows)]
    k = 1
    for i in range(0, nb_rows):
        result[i] = int(line[k])
        k += 1
    return result


# vec is 1xm vector
# matrix is mxn matrix
def matrix_vec_mul(vec, matrix):
    m = len(matrix)
    n = len(matrix[0])
    result = [[0.0 for _ in range(n)]]
    for i in range(0, n):
        for j in range(0, m):
            result[0][i] += vec[0][j] * matrix[j][i]
    for i in range(0, n):
        result[0][i] = round(result[0][i], 10)

    return result