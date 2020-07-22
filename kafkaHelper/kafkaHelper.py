from json import dumps, loads
from kafka import KafkaProducer
from enum import Enum
from kafka import KafkaConsumer
from kafka.errors import KafkaError

class Action(Enum):
    Added = 1
    Modified = 2
    Deleted = 3


def produce(broker_names, topic, data_item):
    producer = KafkaProducer(bootstrap_servers=broker_names,
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8')
                             )
    future = producer.send(topic, data_item)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...

        pass


def consume(broker_names, topic, consumer_group, auto_offset_reset):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker_names,
        auto_offset_reset=auto_offset_reset,
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


