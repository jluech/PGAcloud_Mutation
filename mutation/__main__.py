import logging
import time

from database_handler.handlers import DatabaseHandlers
from database_handler.redis_handler import RedisHandler
from message_handler.handlers import MessageHandlers
from message_handler.rabbit_message_queue import RabbitMessageQueue
from mutation.mutators import Mutators
from utilities import utils

logging.basicConfig(level=logging.INFO)

DATABASE_HANDLER = DatabaseHandlers.Redis
MESSAGE_HANDLER = MessageHandlers.RabbitMQ
MUTATOR = Mutators.BitFlip
RELEVANT_PROPERTIES = ["MUTATION_RATE"]


def listen_for_mutation():
    pga_id = utils.get_pga_id()

    database_handler = get_database_handler(pga_id)
    for prop in RELEVANT_PROPERTIES:
        value = database_handler.retrieve(prop)
        timer = 0
        start = time.perf_counter()
        while value is None and timer < 45:
            time.sleep(1)
            value = database_handler.retrieve(prop)
            timer = time.perf_counter() - start
        if timer >= 10:
            raise Exception("Could not load property: {key_}".format(key_=prop))
        utils.set_property(
            property_key=prop,
            property_value=value.decode("utf-8")
        )

    message_handler = get_message_handler(pga_id)
    message_handler.receive_messages()


def get_database_handler(pga_id):
    if DATABASE_HANDLER == DatabaseHandlers.Redis:
        return RedisHandler(pga_id)
    else:
        raise Exception("No valid DatabaseHandler defined!")


def get_message_handler(pga_id):
    if MESSAGE_HANDLER == MessageHandlers.RabbitMQ:
        return RabbitMessageQueue(pga_id)
    else:
        raise Exception("No valid MessageHandler defined!")


if __name__ == "__main__":
    utils.__set_mutator(MUTATOR)
    listen_for_mutation()
