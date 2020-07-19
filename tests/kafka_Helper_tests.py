import json
import jsonpickle
from kafkaHelper.kafkaHelper import with_action, Action, produce_with_action, consume
from mongoengine import *
broker = "192.168.1.57:9092"
DATE_FORMAT = '%Y-%m-%d'


class user_transaction(Document):
    meta = {'strict': False}
    user_id = IntField()
    volume = LongField()
    symbol = StringField()
    value = LongField()
    price = LongField()
    date = DateField()
    source = StringField()
    currency = StringField()

class user_settings(Document):
    meta = {'strict': False}
    userId = IntField()
    preferred_currency = StringField()


class TestOject():
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)


def test_to_json():
    my_obj = TestOject()
    with_action(my_obj, action=Action.Added,source_id=1)
    assert (my_obj.action == Action.Added)


def test_produce_to_kafka():
    my_obj = TestOject()
    my_obj.id = 10
    with_action(my_obj, action=Action.Added,source_id=1)
    produce_with_action(broker_names=[broker],topic="test_produce_to_kafka",data_item=json.dumps( {'hi' :'there'}   ) )
    items = consume(broker_names=[broker],consumer_group="test_produce_to_kafka", topic="test_produce_to_kafka")
    assert (len(items) == 1)


def test_produce_to_kafka_with_consumer_group():
    my_obj = TestOject()
    my_obj.id = 10
    with_action(my_obj, action=Action.Added,source_id=1)
    produce_with_action(broker_names=[broker],topic="test_produce_to_kafka_with_consumer_group",data_item=json.dumps( {'hi' :'there'}   ) )
    items = consume(broker_names=[broker],consumer_group="test_produce_to_kafka_with_consumer_group",topic="test_produce_to_kafka_with_consumer_group")
    assert (len(items) == 1)


def test_produce_to_kafka_with_consumer_group_2():
    us = user_settings()
    us.userId = 1
    us.preferred_currency = "EUR"
    with_action(us, action=Action.Added,source_id=1)
    print(jsonpickle.encode(us))
    produce_with_action(broker_names=[broker], topic="test_produce_to_kafka_with_consumer_group_2",data_item=jsonpickle.encode(us) )
    items = consume(broker_names=[broker],consumer_group="test_produce_to_kafka_with_consumer_group_2",topic="test_produce_to_kafka_with_consumer_group_2")
    assert (len(items) == 1)

def test_produce_to_kafka_transaction_with_consumer_group_2():
    t = user_transaction()
    t.user_id = 1
    t.preferred_currency = "EUR"
    t.volume = 100
    t.symbol ="BTC"
    t.value = 12131
    t.price = 1213
    t.date = 12121
    t.source = "kraken"
    t.currency = "EUR"
    with_action(t, action=Action.Added,source_id=1)
    produce_with_action(broker_names=[broker],topic="test_produce_to_kafka_transaction_with_consumer_group_2",data_item=jsonpickle.encode(t) )
    items = consume(broker_names=[broker],consumer_group="test_produce_to_kafka_transaction_with_consumer_group_2",topic="test_produce_to_kafka_transaction_with_consumer_group_2")
    assert (len(items) == 1)
    for trans in items:
        da_item = jsonpickle.decode(trans,keys=False)
        assert (da_item.value == 12131)
        assert (da_item.symbol == "BTC")


def test_produce_to_kafka_transaction_with_consumer_group_two_items():
    t = user_transaction()
    t.user_id = 1
    t.preferred_currency = "EUR"
    t.volume = 100
    t.symbol ="BTC"
    t.value = 12131
    t.price = 1213
    t.date = 12121
    t.source = "kraken"
    t.currency = "EUR"
    with_action(t, action=Action.Added,source_id=1)
    produce_with_action(broker_names=[broker],topic="test_produce_to_kafka_transaction_with_consumer_group_two_items",data_item=jsonpickle.encode(t) )
    produce_with_action(broker_names=[broker],topic="test_produce_to_kafka_transaction_with_consumer_group_two_items",data_item=jsonpickle.encode(t) )
    items = consume(broker_names=[broker],consumer_group="test_produce_to_kafka_transaction_with_consumer_group_two_items",topic="test_produce_to_kafka_transaction_with_consumer_group_two_items")
    assert (len(items) == 2)
    for trans in items:
        print(trans)
        da_item = jsonpickle.decode(trans, keys=False)
        print(da_item)
        assert (da_item.value == 12131)
        assert (da_item.symbol == "BTC")

