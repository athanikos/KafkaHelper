from json import dumps, loads
from kafka import KafkaProducer
from enum import Enum
import jsonpickle
from kafka import KafkaConsumer


class Action(Enum):
    Added = 1
    Modified = 2
    Deleted = 3


def with_action(data_item, action, source_id):
    if data_item is None:
        raise ValueError(" does not exist ")
    setattr(data_item, 'action', action)
    setattr(data_item, 'source_id', source_id)
    return jsonpickle.encode(data_item)


def produce_with_action(broker_names, topic, data_item):
    producer = KafkaProducer(bootstrap_servers=broker_names,
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    producer.send(topic, data_item)


def consume(broker_names, topic, consumer_group):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker_names,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        auto_commit_interval_ms=1,
        group_id=consumer_group,
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        consumer_timeout_ms=3000
        )
    items = []
    for msg in consumer:
        items.append(msg.value)
    return items


