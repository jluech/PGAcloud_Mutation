import logging
import random
from abc import ABC, abstractmethod
from distutils.util import strtobool


class AbstractMutation(ABC):
    @ abstractmethod
    def perform_mutation(self, individual, mutation_rate):
        # Perform the mutation on an Individual.
        # Returns a potentially mutated Individual.
        pass


class BitFlipMutation(AbstractMutation):
    def perform_mutation(self, individual, mutation_rate):
        length = individual.solution.__len__()
        flips_amount = random.randint(1, length)
        logging.info("Mutating individual '{ind_}' at {amount_} positions.".format(
            ind_=individual.solution,
            amount_=flips_amount,
        ))
        for i in range(0, flips_amount):
            flip_position = random.randint(0, length)
            individual.solution[flip_position] = not strtobool(individual.solution[flip_position])
        logging.debug(individual.solution)
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
