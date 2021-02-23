#!/usr/bin/env python3
import math
from time import time

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
import hmm_model





class PlayerControllerHMM(PlayerControllerHMMAbstract):

    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.guessed_fishes_dict = {}
        self.train_index = 0

    def init_models(self,observations):
        self.models = []
        for i in range(0,len(observations)):
            self.models.append(hmm_model.Hmm_model())

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
        self.time_start = time()
        if step ==1:
            self.init_models(observations)
        guess= None
        if (N_STEPS-step<=N_FISH):
            guess =  self.closest_already_guessed()
        for fish_id in range(0,N_FISH):
            self.models[fish_id].add_emmissions_no_train(observations[fish_id])
        if step>1:
            while time() - self.time_start<0.1:
                self.models[self.train_index].train(1)
                self.train_index+=1
                if self.train_index == N_FISH:
                    self.train_index=0
        return guess

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        self.guessed_fishes_dict[fish_id] = true_type

    def closest_already_guessed(self):
        if (len(self.guessed_fishes_dict) == 0):
            #print("random")
            return (0, random.randint(0, N_SPECIES - 1))  #random guess

        min_dist = math.inf
        best_fish = 0
        best_fish_type = 0
        for fish_id in range(0,N_FISH):
            if not fish_id in self.guessed_fishes_dict.keys():
                for candidate_fish_id in self.guessed_fishes_dict.keys():
                    dist = self.distance(self.models[fish_id],self.models[candidate_fish_id])
                    if (dist<min_dist):
                        min_dist = dist
                        best_fish = fish_id
                        best_fish_type = self.guessed_fishes_dict[candidate_fish_id]
        return (best_fish,best_fish_type)


    def distance(self, model1, model2):
        A_dist = self.sqe(model1.A,model2.A)
        B_dist = self.sqe(model1.B,model2.B)
        return A_dist + B_dist

    def sqe(self, matrix, other_matrix):
        sqe = 0
        m = len(matrix)
        n = len(matrix[0])
        result = {}
        for i in range(m):
            min = math.inf
            for k in range(m):
                rowmse = 0
                for j in range(n):
                    rowmse += math.pow(matrix[i][j] - other_matrix[k][j], 2)
                if (rowmse < min and k not in result.values()):
                    min = rowmse
                    result[i] = k
            sqe+= min
        return sqe











