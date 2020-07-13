from json import dumps
from kafka import KafkaProducer
from enum import Enum


class Action(Enum):
    Added = 1
    Modified = 2
    Deleted = 3


def produce_transaction_with_action(broker_names, topic,  data_item, action):
    data_item.set_attr('action', action)
    producer = KafkaProducer(bootstrap_servers=[broker_names],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    producer.send(topic, data_item)


