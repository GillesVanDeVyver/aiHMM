from sys import stdin
import matrix


def main():
    A = matrix.create_matrix(stdin.readline().split())
    B = matrix.create_matrix(stdin.readline().split())
    pi = matrix.create_matrix(stdin.readline().split())
    v1 = matrix.matrix_vec_mul(pi, A)
    v2 = matrix.matrix_vec_mul(v1, B)
    n = len(v2[0])
    result = "1 " + str(n)
    for i in range(0, n):
        result += " " + str(v2[0][i])
    print(result)
    return result


if __name__ == "__main__":
    main()
