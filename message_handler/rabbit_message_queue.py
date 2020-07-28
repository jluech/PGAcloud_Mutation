import json
import logging

import pika

from message_handler.message_handler import MessageHandler
from mutation.mutation import apply_mutation
from population.individual import Individual, IndividualEncoder
from utilities import utils


def receive_mutation_callback(channel, method, properties, body):
    queue_name = utils.get_messaging_source()

    ind_dict = json.loads(body)
    individual = Individual(ind_dict["solution"], ind_dict["fitness"])
    logging.info("rMQ:{queue_}: Received mutation request for individual: {ind_}".format(
        queue_=queue_name,
        ind_=individual,
    ))

    mutated_individual = apply_mutation(individual)

    send_message_to_queue(
        channel=channel,
        payload=mutated_individual
    )


def send_message_to_queue(channel, payload):
    # Route the message to the next queue in the model.
    # next_recipient = utils.get_messaging_target()
    next_recipient = "generation"  # TODO: replace with original
    channel.queue_declare(queue=next_recipient, auto_delete=True, durable=True)

    # Send message to given recipient.
    logging.info("rMQ: Sending '{body_}' to {dest_}.".format(
        body_=payload,
        dest_=next_recipient,
    ))
    channel.basic_publish(
        exchange="",
        routing_key=next_recipient,
        body=json.dumps(payload, cls=IndividualEncoder),
        # Delivery mode 2 makes the broker save the message to disk.
        # This will ensure that the message be restored on reboot even
        # if RabbitMQ crashes before having forwarded the message.
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )


class RabbitMessageQueue(MessageHandler):
    def __init__(self, pga_id):
        # Establish connection to rabbitMQ.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitMQ--{id_}".format(id_=pga_id),
            socket_timeout=30,
        ))

    def receive_messages(self):
        # Define communication channel.
        channel = self.connection.channel()

        # Create queue for mutation.
        queue_name = utils.get_messaging_source()
        channel.queue_declare(queue=queue_name, auto_delete=True, durable=True)

        # Actively listen for messages in queue and perform callback on receive.
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=receive_mutation_callback,
        )
        logging.info("rMQ:{queue_}: Waiting for mutation requests.".format(
            queue_=queue_name
        ))
        channel.start_consuming()

        # Close connection when finished. TODO: check if prematurely closing connection
        logging.info("rMQ: CLOSING CONNECTION")
        self.connection.close()

    def send_message(self, individual):
        # Define communication channel.
        channel = self.connection.channel()
        send_message_to_queue(
            channel=channel,
            payload=individual
        )
