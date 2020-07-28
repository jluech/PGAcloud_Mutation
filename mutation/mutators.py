import logging
import random
from abc import ABC, abstractmethod
from distutils.util import strtobool
from enum import Enum


class Mutators(Enum):
    BitFlip = "bit_flip",
    Inversion = "inversion",
    Scramble = "scramble",
    Swap = "swap",


class AbstractMutation(ABC):
    @ abstractmethod
    def perform_mutation(self, individual, mutation_rate):
        # Perform the mutation on an Individual.
        # Returns a potentially mutated Individual.
        pass


class BitFlipMutation(AbstractMutation):
    def perform_mutation(self, individual, mutation_rate):
        mutation_chance = random.randint(0, 100) / 100
        # logging.info("Mutation chance = " + str(mutation_chance))
        mutation_occurred = (mutation_rate >= mutation_chance)

        if mutation_occurred:
            length = individual.solution.__len__()
            flips_amount = random.randint(1, length)
            logging.info("Mutating individual '{ind_}' at {amount_} position(s).".format(
                ind_=individual.solution,
                amount_=flips_amount,
            ))
            for flip in range(0, flips_amount):
                flip_position = random.randint(0, length-1)
                if strtobool(individual.solution[flip_position]):
                    individual.solution = individual.solution[:flip_position] + "0" + individual.solution[flip_position+1:]
                else:
                    individual.solution = individual.solution[:flip_position] + "1" + individual.solution[flip_position+1:]
        else:
            logging.info("Mutation of individual '{ind_}' did not occur.".format(ind_=individual.solution))
        return individual


class InversionMutation(AbstractMutation):
    def perform_mutation(self, individual, mutation_rate):
        pass


class ScrambleMutation(AbstractMutation):
    def perform_mutation(self, individual, mutation_rate):
        pass


class SwapMutation(AbstractMutation):
    def perform_mutation(self, individual, mutation_rate):
        pass
