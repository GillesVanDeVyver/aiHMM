from constants import *

from hmm_model import *

N = 3





class Centroid():

    def __init__(self):
        self.summed_A = [[0 for _ in range(0,N)] for _ in range(0,N)]
        self.summed_B = [[0 for _ in range(0, N_EMISSIONS)] for _ in range(0, N)]
        self.centerA = [[0 for _ in range(0,N)] for _ in range(0,N)]
        self.centerB = [[0 for _ in range(0,N_EMISSIONS)] for _ in range(0,N)]
        self.nb_fishes =0

    def find_corrseponding_states(self,matrix, other_matrix):
        n = len(matrix[0])
        result = {}
        for i in range(N):
            min = math.inf
            for k in range(N):
                rowmse = 0
                for j in range(n):
                    rowmse += math.pow(matrix[i][j] - other_matrix[k][j], 2)
                if rowmse < min and k not in result.values():
                    min = rowmse
                    result[i] = k
        return result

    def add_model(self, model: Hmm_model):
        self.nb_fishes+=1

        state_permutation = self.find_corrseponding_states(self.summed_B,model.B)


        for i in range(0,N):
            for j in range(0, N):
                self.summed_A[state_permutation[i]][j] += model.A[i][j]
        for i in range(0, N):
            for j in range(0, N_EMISSIONS):
                self.summed_B[state_permutation[i]][j] += model.B[i][j]
        for i in range(0,N):
            for j in range(0, N):
                self.centerA[i][j] = self.summed_A[i][j]/self.nb_fishes
        for i in range(0, N):
            for j in range(0, N_EMISSIONS):
                self.centerB[i][j] = self.summed_B[i][j] / self.nb_fishes

    def distance(self, model: Hmm_model):
        A_dist = self.mse(model.A,self.centerA)
        B_dist = self.mse(model.B,self.centerB)
        return A_dist + B_dist

    def mse(self, matrix, other_matrix):
        mse = 0
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            min = math.inf
            for k in range(m):
                rowmse = 0
                for j in range(n):
                    rowmse += math.pow(matrix[i][j] - other_matrix[k][j], 2)
                if (rowmse < min):
                    min = rowmse
            mse+= min
        return mse / (m * n)













