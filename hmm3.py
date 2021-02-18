from sys import stdin
from math import log
import matrix


def main():
    A = matrix.create_matrix(stdin.readline().split())
    B = matrix.create_matrix(stdin.readline().split())
    pi = matrix.create_matrix(stdin.readline().split())
    emissions = matrix.create_vector(stdin.readline().split())
    T = len(emissions)
    N = len(A)
    K = len(B[0])
    alpha = [[0.0 for _ in range(N)] for _ in range(T)]
    beta = [[0.0 for _ in range(N)] for _ in range(T)]
    di_gamma = [[[0.0 for _ in range(N)] for _ in range(N)] for _ in range(T-1)]
    gamma = [[0.0 for _ in range(N)] for _ in range(T)]
    scaling_factors = [0.0 for _ in range(T)]
    max_its = 30
    its = 0
    old_log_prob = -float("inf")
    range_n = range(N)

    while its < max_its:  # its < max_its:
        scaling_factors[0] = 0
        for i in range_n:
            temp = B[i][emissions[0]] * pi[0][i]
            alpha[0][i] = temp
            scaling_factors[0] += temp

        scaling_factors[0] = 1 / scaling_factors[0]
        alpha[0] = [x * scaling_factors[0] for x in alpha[0]]

        log_prob = log(scaling_factors[0])
        for t in range(1, T):
            scaling_factors[t] = 0
            for i in range_n:
                s = 0
                for j in range_n:
                    s += A[j][i] * alpha[t-1][j]
                alpha[t][i] = B[i][emissions[t]] * s
                scaling_factors[t] += alpha[t][i]
            scaling_factors[t] = 1 / scaling_factors[t]
            alpha[t] = [x * scaling_factors[t] for x in alpha[t]]
            log_prob += log(scaling_factors[t])
        log_prob = -log_prob

        if log_prob > old_log_prob:
            old_log_prob = log_prob
            # its += its
        else:
            break

        beta[T-1] = [scaling_factors[T-1] for _ in range_n]  # 1 scaled by cT-1

        for t in reversed(range(T-1)):
            for i in range(N):
                s = 0
                for j in range(N):
                    s += beta[t+1][j] * B[j][emissions[t+1]] * A[i][j]
                beta[t][i] = s * scaling_factors[t]

        for t in range(T-1):
            for i in range_n:
                di_gamma_sum = 0
                for j in range_n:
                    temp = alpha[t][i] * A[i][j] * B[j][emissions[t+1]] * beta[t+1][j]
                    di_gamma[t][i][j] = temp
                    di_gamma_sum += temp
                gamma[t][i] = di_gamma_sum

        gamma[T-1] = alpha[T-1]

        for i in range_n:
            pi[0][i] = gamma[0][i]
            gamma_sum = 0
            for t in range(T-1):
                gamma_sum += gamma[t][i]
            for k in range(K):
                ind_gamma_sum = 0
                for t in range(T):
                    if emissions[t] == k:
                        ind_gamma_sum += gamma[t][i]
                B[i][k] = ind_gamma_sum / gamma_sum
            for j in range_n:
                di_gamma_sum = 0
                for t in range(T-1):
                    di_gamma_sum += di_gamma[t][i][j]
                A[i][j] = di_gamma_sum / gamma_sum
        its+=1

    result = str(N) + " " + str(N)
    for row in A:
        for val in row:
            result += " " + str(round(val, 6))
    result += "\n" + str(N) + " " + str(K)
    for row in B:
        for val in row:
            result += " " + str(round(val, 6))

    print(result)
    return result


if __name__ == "__main__":
    main()
