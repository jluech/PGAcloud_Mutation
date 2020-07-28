import logging

from mutation.mutators import Mutators, BitFlipMutation, InversionMutation, ScrambleMutation, SwapMutation
from utilities.utils import forward_mutator, get_property


def apply_mutation(individual):
    # Applies the chosen mutation operator on the two individuals and returns a pair {ind1: x, ind2: y}
    logging.info("Performing mutation on individual: {ind_}".format(
        ind_=individual
    ))

    mutator = get_mutator()
    mutation_rate = get_mutation_rate()
    return mutator.perform_mutation(individual, mutation_rate)


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
