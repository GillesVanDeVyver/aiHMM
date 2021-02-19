import math
import random
from math import log
import matrix
from constants import *


N = 3

class Hmm_model():

    # k = nb of possible obs
    def __init__(self, first_obs):
        self.A = self.uniform(N, N)
        self.B = self.uniform(N, N_EMISSIONS)
        self.pi = self.uniform(1, N)
        self.add_random_noise(self.A)
        self.add_random_noise(self.B)
        self.add_random_noise(self.pi)
        self.emissions = []


    def aplha_pass(self, range_n, T):
        self.scaling_factors[0] = 0

        #if all_zero(B[i]):


        for i in range_n:
            temp = self.B[i][self.emissions[0]] * self.pi[0][i]
            self.alpha[0][i] = temp
            self.scaling_factors[0] += temp

        if self.scaling_factors[0] == 0:
            self.scaling_factors[0] = 1/N
            self.alpha[0] = [x * self.scaling_factors[0] for x in self.alpha[0]]
            self.add_random_noise_vector(self.alpha[0])
        else:
            self.scaling_factors[0] = 1 / self.scaling_factors[0]
            self.alpha[0] = [x * self.scaling_factors[0] for x in self.alpha[0]]

        log_prob = log(self.scaling_factors[0])
        for t in range(1, T):
            self.scaling_factors[t] = 0
            for i in range_n:
                s = 0
                for j in range_n:
                    s += self.A[j][i] * self.alpha[t - 1][j]
                self.alpha[t][i] = self.B[i][self.emissions[t]] * s
                self.scaling_factors[t] += self.alpha[t][i]

            if self.scaling_factors[t] == 0:  # this observation never occured => whole col of B
                self.alpha[t] = [x*1/N for x in self.alpha[t]]
                self.add_random_noise_vector(self.alpha[t])
                log_prob += log(1/N)
            else:
                self.scaling_factors[t] = 1 / self.scaling_factors[t]
                self.alpha[t] = [x * self.scaling_factors[t] for x in self.alpha[t]]
                print(self.alpha[t])
                log_prob += log(self.scaling_factors[t])
        return -log_prob


    def beta_pass(self, T, range_n, N ):
        self.beta[T - 1] = [self.scaling_factors[T - 1] for _ in range_n]  # 1 scaled by cT-1

        for t in reversed(range(T - 1)):
            for i in range(N):
                s = 0
                for j in range(N):
                    s += self.beta[t + 1][j] * self.B[j][self.emissions[t + 1]] * self.A[i][j]
                self.beta[t][i] = s * self.scaling_factors[t]


    def compute_gamma(self,T, range_n):
        for t in range(T - 1):
            for i in range_n:
                di_gamma_sum = 0
                for j in range_n:
                    temp = self.alpha[t][i] * self.A[i][j] * self.B[j][self.emissions[t + 1]] * self.beta[t + 1][j]
                    self.di_gamma[t][i][j] = temp
                    di_gamma_sum += temp
                self.gamma[t][i] = di_gamma_sum

        self.gamma[T - 1] = self.alpha[T - 1]


    def reestimate(self,range_n,T):
        for i in range_n:
            self.pi[0][i] = self.gamma[0][i]
            gamma_sum = 0
            for t in range(T - 1):
                gamma_sum += self.gamma[t][i]
            for k in range(N_EMISSIONS):
                ind_gamma_sum = 0
                for t in range(T):
                    if self.emissions[t] == k:
                        ind_gamma_sum += self.gamma[t][i]
                if gamma_sum == 0:  # fix for diagonal init
                    self.B[i][k] = 1 / (N_EMISSIONS)
                else:
                    self.B[i][k] = ind_gamma_sum / gamma_sum
            for j in range_n:
                di_gamma_sum = 0
                for t in range(T - 1):
                    di_gamma_sum += self.di_gamma[t][i][j]
                if gamma_sum == 0:  # fix for diagonal init
                    self.A[i][j] = 1 / (len(self.A))
                else:
                    self.A[i][j] = di_gamma_sum / gamma_sum


    # mean square error
    def mse(self,matrix, other_matrix):
        mse = 0
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            for j in range(n):
                min = math.inf
                for k in range(m):
                    rowmse = math.pow(matrix[i][j] - other_matrix[i][j], 2)
                    if (rowmse < mse):
                        mse = rowmse
                mse += rowmse
        return mse / (m * n)


    def uniform(self,m, n):
        val = 1 / (n)
        return [[val for x in range(n)] for y in range(m)]


    def add_random_noise(self,matrix):
        val = matrix[0][0]
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            rowStoch = 0
            for j in range(n - 1):
                randVal = random.uniform(-val, val) / n
                rowStoch -= randVal
                matrix[i][j] += randVal
            matrix[i][n - 1] += rowStoch

    def add_random_noise_vector(self,vec):
        val = vec[0]
        m = len(vec)
        rowStoch = 0
        for i in range(m-1):
            randVal = random.uniform(-val, val) / m
            rowStoch -= randVal
            vec[i] += randVal
        vec[m - 1] += rowStoch

    def identity(self,n):
        m = [[0 for x in range(n)] for y in range(n)]
        for i in range(0, n):
            m[i][i] = 1
        return m


    def add_emmissions_no_train(self, new_obs):
        self.emissions.append(new_obs)


    def train(self, max_its, new_obs):
        self.emissions.append(new_obs)
        T = len(self.emissions)
        print("T = " + str(T))

        self.scaling_factors = [0.0 for _ in range(T)]
        N = 3
        self.alpha = [[0.0 for _ in range(N)] for _ in range(T)]
        self.beta = [[0.0 for _ in range(N)] for _ in range(T)]
        self.di_gamma = [[[0.0 for _ in range(N)] for _ in range(N)] for _ in range(T - 1)]
        self.gamma = [[0.0 for _ in range(N)] for _ in range(T)]

        its = 0
        old_log_prob = -float("inf")
        range_n = range(N)
        while its < max_its:
            log_prob = self.aplha_pass(range_n, T)
            # print("log_prob: " + str(log_prob))
            if log_prob > old_log_prob + 1E-2:
                old_log_prob = log_prob
            else:
                break
            self.beta_pass(T, range_n, N)
            self.compute_gamma(T, range_n)
            self.reestimate(range_n,T)
            its += 1