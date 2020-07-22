import logging

from mutation.mutators import BitFlipMutation, InversionMutation, ScrambleMutation, SwapMutation
from population.pair import Pair
from utilities.utils import Mutators, forward_mutator, get_property


def apply_mutation(individual1, individual2):
    # Applies the chosen mutation operator on the two individuals and returns a pair {ind1: x, ind2: y}
    logging.info("Performing mutation on individuals:")
    logging.info("{ind_}".format(
        ind_=individual1
    ))
    logging.info("{ind_}".format(
        ind_=individual2
    ))

    mutator = get_mutator()
    mutation_rate = get_mutation_rate()
    ind1 = mutator.perform_mutation(individual1, mutation_rate)
    ind2 = mutator.perform_mutation(individual2, mutation_rate)

    return Pair(ind1, ind2)


def get_mutator():
    mutator = forward_mutator()
    if mutator == Mutators.BitFlip:
        return BitFlipMutation()
    elif mutator == Mutators.Inversion:
        __mutator = InversionMutation()
        raise Exception("InversionMutation not implemented yet!")
    elif mutator == Mutators.Scramble:
        __mutator = ScrambleMutation()
        raise Exception("ScrambleMutation not implemented yet!")
    elif mutator == Mutators.Swap:
        __mutator = SwapMutation()
        raise Exception("SwapMutation not implemented yet!")
    else:
        raise Exception("No valid Mutator defined!")


def get_mutation_rate():
    rate = float(get_property("MUTATION_RATE"))
    logging.info("MUTATION_RATE={_rate} retrieved.".format(_rate=rate))
    return rate
