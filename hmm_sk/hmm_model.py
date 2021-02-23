import math
import random
from math import log
import matrix
from constants import *


N =5





class Hmm_model():

    def __init__(self):
        self.A = self.uniform(N, N)
        self.B = self.uniform(N, N_EMISSIONS)
        self.pi = self.uniform(1, N)
        self.add_random_noise(self.A)
        self.add_random_noise(self.B)
        self.add_random_noise(self.pi)
        self.emissions = []

    def aplha_pass(self, range_n, T):
        self.scaling_factors[0] = 0
        for i in range_n:
            temp = self.B[i][self.emissions[0]] * self.pi[0][i]
            self.alpha[0][i] = temp
            self.scaling_factors[0] += temp

        if self.scaling_factors[0] == 0:
            self.scaling_factors[0] = 1 / N
        else:
            self.scaling_factors[0] = 1 / self.scaling_factors[0]
        self.alpha[0] = [x * self.scaling_factors[0] for x in self.alpha[0]]
        for t in range(1, T):
            self.scaling_factors[t] = 0
            for i in range_n:
                s = 0
                for j in range_n:
                    s += self.A[j][i] * self.alpha[t - 1][j]
                self.alpha[t][i] = self.B[i][self.emissions[t]] * s
                self.scaling_factors[t] += self.alpha[t][i]
            if self.scaling_factors[t] == 0:
                self.scaling_factors[t] = 1 / N
            else:
                self.scaling_factors[t] = 1 / self.scaling_factors[t]
            self.alpha[t] = [x * self.scaling_factors[t] for x in self.alpha[t]]

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
            if self.all_zero_vec(self.gamma[t]):
                self.gamma[t] = self.uniform_vec(N)
                self.add_random_noise_vector(self.gamma[t])
        self.gamma[T - 1] = self.alpha[T - 1]

    def all_zero_vec(self, vec):
        for el in vec:
            if el != 0:
                return False
        return True

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
                self.B[i][k] = round(ind_gamma_sum / gamma_sum,2)
            for j in range_n:
                di_gamma_sum = 0
                for t in range(T - 1):
                    di_gamma_sum += self.di_gamma[t][i][j]
                self.A[i][j] = round(di_gamma_sum / gamma_sum,2)

    def uniform(self,m, n):
        val = 1 / (n)
        return [[val for x in range(n)] for y in range(m)]

    def uniform_vec(self, n):
        val = 1 / (n)
        return [val for x in range(n)]

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

    def add_emmissions_no_train(self, new_obs):
        self.emissions.append(new_obs)

    def train(self, max_its):
        T = len(self.emissions)

        self.scaling_factors = [0.0 for _ in range(T)]
        self.alpha = [[0.0 for _ in range(N)] for _ in range(T)]
        self.beta = [[0.0 for _ in range(N)] for _ in range(T)]
        self.di_gamma = [[[0.0 for _ in range(N)] for _ in range(N)] for _ in range(T - 1)]
        self.gamma = [[0.0 for _ in range(N)] for _ in range(T)]

        its = 0
        range_n = range(N)
        while its < max_its:
            #self.check()
            self.aplha_pass(range_n, T)
            self.beta_pass(T, range_n, N)
            self.compute_gamma(T, range_n)
            self.reestimate(range_n,T)
            its += 1




