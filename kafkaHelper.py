from json import dumps
from kafka import KafkaProducer
from enum import Enum
import jsonpickle
from kafka import KafkaConsumer

class Action(Enum):
    Added = 1
    Modified = 2
    Deleted = 3


def to_json_with_action(data_item, action):
    if data_item is None:
        raise ValueError(" does not exist ")
    setattr(data_item,'action', action)
    item =  jsonpickle.encode(data_item)
    print(item)


def produce_with_action(broker_names, topic,  data_item):
    producer = KafkaProducer(bootstrap_servers=[broker_names],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    producer.send(topic, to_json_with_action(data_item =data_item) )


def consume(broker_names, topic,  consumer_group):
    consumer = KafkaConsumer('my_favorite_topic', group_id='my_favorite_group')
    items = []
    for msg in consumer:
        items.append(msg)
    return items