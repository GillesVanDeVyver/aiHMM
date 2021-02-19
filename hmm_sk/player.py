#!/usr/bin/env python3

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
        pass

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
        # value of obs 0-7 => 8 possible observations/emmissions

        if step ==1:
            self.init_models(observations)


        if (step>5):
            for i in range(0,N_EMISSIONS):
                self.models[i].train(5,observations[i])
        else:
            for i in range(0,N_EMISSIONS):
                self.models[i].add_emmissions_no_train(observations[i])

        print("A" + str(self.models[3].A))
        print("B" + str(self.models[3].B))


        # This code would make a random guess on each step:
        #print((observations))
        return (step % N_FISH, random.randint(0, N_SPECIES - 1))

        #return None

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
        pass


"""
___________DEV NOTES___________


current main issue: when new observation occurs (not yet seen for this fish)
all scaling factors all zero => initiliaze as uniform? => problem local maxima unifrom

=> TODO add noise to this vector?


Basic idea:
1 hmm model for each fish.
On each new observation, train the model for a few iterations.
first obs: initialize unifrom + noise
Start with model from previous observations        note: stuck in local minima? Maybe reInitialize random? => later
Once we now some fishes we can geuss that fishes with small mse are the same species

Note: when to do guessing?

Note: how much iterations to do in each obs? Each fish same amount of obs? Keep track of time?

Note: the futher in the game the more obs => longer time/iter => less iter?

(Note: mse for pi is wrong)

"""













