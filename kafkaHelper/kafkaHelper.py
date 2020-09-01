from json import dumps, loads
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError


def produce(broker_names, topic, data_item):
    producer = KafkaProducer(bootstrap_servers=broker_names,
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8')
                             )
    future = producer.send(topic, value=data_item)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        raise


def produce_with_key(broker_names, topic, data_item, key):
    producer = KafkaProducer(bootstrap_servers=broker_names,
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8')
                             )
    future = producer.send(topic, value=data_item, key=key)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        raise


def consume(broker_names, topic, consumer_group, auto_offset_reset, consumer_timeout_ms):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker_names,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=True,
        auto_commit_interval_ms=1,
        group_id=consumer_group,
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        consumer_timeout_ms=consumer_timeout_ms
    )
    items = []
    for msg in consumer:
        items.append(msg.value)
    return items
