import math
import random
from copy import deepcopy
from sys import stdin
from math import log
import matrix


correct_A = [[0.7 , 0.05, 0.25],
            [0.1 , 0.8 , 0.1],
            [0.2 , 0.3 , 0.5]]

correct_B = [[0.7 , 0.2 , 0.1 , 0  ],
            [0.1 , 0.4 , 0.3 , 0.2],
            [0   , 0.1 , 0.2,  0.7]]

correct_pi = [[1  , 0  , 0  ]]

A_close =  [[0.71 , 0.06, 0.23],
            [0.11 , 0.81 , 0.08],
            [0.21 , 0.31 , 0.48]]

B_close =  [[0.71 , 0.19 , 0.09 , 0.01  ],
            [0.11 , 0.39 , 0.31 , 0.19],
            [0.01   , 0.09 , 0.21,  0.69]]

pi_close =  [[0.98  , 0.01  , 0.01  ]]

A =        [[0.54, 0.26, 0.2 ],
            [0.19, 0.53, 0.28],
            [0.22, 0.18, 0.6 ]]

B =        [[0.5 , 0.2 , 0.11, 0.19],
            [0.22, 0.28, 0.23, 0.27],
            [0.19, 0.21, 0.15, 0.45]]

pi =        [[0.3  , 0.2  , 0.5  ]]

def aplha_pass(scaling_factors, range_n, B, emissions, pi, alpha,A, T_stop, T_start = 0):
    emissionsUsed = emissions[T_start:T_stop]
    T= len(emissionsUsed)

    scaling_factors[0] = 0
    for i in range_n:
        temp = B[i][emissionsUsed[0]] * pi[0][i]
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
                s += A[j][i] * alpha[t - 1][j]
            alpha[t][i] = B[i][emissionsUsed[t]] * s
            scaling_factors[t] += alpha[t][i]
        scaling_factors[t] = 1 / scaling_factors[t]
        alpha[t] = [x * scaling_factors[t] for x in alpha[t]]
        log_prob += log(scaling_factors[t])
    return -log_prob

def beta_pass(beta, T, scaling_factors, range_n, N, B, emissions, A):
    beta[T - 1] = [scaling_factors[T - 1] for _ in range_n]  # 1 scaled by cT-1

    for t in reversed(range(T - 1)):
        for i in range(N):
            s = 0
            for j in range(N):
                s += beta[t + 1][j] * B[j][emissions[t + 1]] * A[i][j]
            beta[t][i] = s * scaling_factors[t]

def compute_gamma(T, range_n, alpha, A, B, emissions, beta, di_gamma, gamma):
    for t in range(T - 1):
        for i in range_n:
            di_gamma_sum = 0
            for j in range_n:
                temp = alpha[t][i] * A[i][j] * B[j][emissions[t + 1]] * beta[t + 1][j]
                di_gamma[t][i][j] = temp
                di_gamma_sum += temp
            gamma[t][i] = di_gamma_sum

    gamma[T - 1] = alpha[T - 1]


def reestimate(range_n, pi, gamma, T, emissions, B, di_gamma, A, K):
    for i in range_n:
        pi[0][i] = gamma[0][i]
        gamma_sum = 0
        for t in range(T - 1):
            gamma_sum += gamma[t][i]
        for k in range(K):
            ind_gamma_sum = 0
            for t in range(T):
                if emissions[t] == k:
                    ind_gamma_sum += gamma[t][i]
            if gamma_sum==0: # fix for diagonal init
                B[i][k]=1/(K)
            else:
                B[i][k] = ind_gamma_sum / gamma_sum
        for j in range_n:
            di_gamma_sum = 0
            for t in range(T - 1):
                di_gamma_sum += di_gamma[t][i][j]
            if gamma_sum==0: # fix for diagonal init
                A[i][j]=1/(len(A))
            else:
                A[i][j] = di_gamma_sum / gamma_sum


# mean square error
def mse(matrix, correctMatrix):
    mse = 0
    m = len(matrix)
    n = len(matrix[0])
    for i in range(m):
        for j in range(n):
            min = math.inf
            for k in range(m):
                rowmse = math.pow(matrix[i][j] - correctMatrix[i][j],2)
                if (rowmse<mse):
                    mse = rowmse

            mse+=rowmse
    return mse/(m*n)


def uniform(m, n):
    val = 1/(n)
    return  [[val for x in range(n)] for y in range(m)]


def add_stochastic_noise(matrix):
    val = matrix[0][0]
    m = len(matrix)
    n = len(matrix[0])
    for i in range(m):
        rowStoch = 0
        for j in range(n-1):
            randVal = random.uniform(-val, val)/n
            rowStoch-=randVal
            matrix[i][j] += randVal
        matrix[i][n-1]+=rowStoch

def identity(n):
    m=[[0 for x in range(n)] for y in range(n)]
    for i in range(0,n):
        m[i][i] = 1
    return m


def main():
    emissions = matrix.create_vector(stdin.readline().split())
    T_total = len(emissions)

    T_train = round(T_total *0.75)


    K = 4 #nb of possible emissions

    scaling_factors = [0.0 for _ in range(T_train)]
    max_its = math.inf

    #for N in range(1,10):
    N = 3
    alpha = [[0.0 for _ in range(N)] for _ in range(T_train)]
    beta = [[0.0 for _ in range(N)] for _ in range(T_train)]
    di_gamma = [[[0.0 for _ in range(N)] for _ in range(N)] for _ in range(T_train - 1)]
    gamma = [[0.0 for _ in range(N)] for _ in range(T_train)]


    # initial guesses
    # https://stackoverflow.com/questions/13966699/hidden-markov-model-initial-guess
    # here stochastic
    A = uniform(N,N)
    B = uniform(N,K)
    pi = uniform(1,N)

    #add_stochastic_noise(A)
    #add_stochastic_noise(B)
    #add_stochastic_noise(pi)

    #diagonal
    #A = identity(N)
    #pi = [[0,0,1]]

    # close to solution
    A = A_close
    B = B_close
    pi = pi_close

    # exact solution for testing
    #A = deepcopy(correct_A)
    #B = deepcopy(correct_B)
    #pi = deepcopy(correct_pi)

    its = 0
    old_log_prob = -float("inf")
    range_n = range(N)

    while its < max_its:
        log_prob = aplha_pass(scaling_factors, range_n, B, emissions, pi, alpha, A, T_train)
        #print("log_prob: " + str(log_prob))
        if log_prob > old_log_prob + 1E-2:
            old_log_prob = log_prob
        else:
            break
        beta_pass(beta, T_train, scaling_factors, range_n, N, B, emissions, A)
        compute_gamma(T_train, range_n, alpha, A, B, emissions, beta, di_gamma, gamma)
        reestimate(range_n, pi, gamma, T_train, emissions, B, di_gamma, A, K)
        its+=1
    print("A: " + str(A))
    print("B: " + str(B))
    print("pi: "+ str(pi))
    #print("number of states: " + str(N))

    print("final log prob train: " + str(old_log_prob))
    print("mse A: " + str(mse(A, correct_A)))
    print("mse B: " + str(mse(B, correct_B)))
    print("mse pi: " + str(mse(pi, correct_pi)))
    # another goodness criteria would be number of right most likely observations
    print("iterations until convergence: " + str(its))

    scaling_factors_test = [0.0 for _ in range(T_total-T_train)]

    log_prob_test = aplha_pass(scaling_factors_test, range_n, B, emissions, pi, alpha, A, T_total, T_train)
    print("final log prob test: " + str(log_prob_test))


if __name__ == "__main__":
    main()