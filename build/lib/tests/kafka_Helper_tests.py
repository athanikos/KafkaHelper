import json

import jsonpickle
from flask import jsonify

from kafkaHelper.kafkaHelper import with_action, Action, produce_with_action, consume
from mongoengine import *


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
    with_action(my_obj, action=Action.Added)
    assert (my_obj.action == Action.Added)


def test_produce_to_kafka():
    my_obj = TestOject()
    my_obj.id = 10
    with_action(my_obj, action=Action.Added)
    produce_with_action(broker_names=["localhost:9092"],topic="testme",data_item=json.dumps( {'hi' :'there'}   ), id=my_obj.id )
    items = consume(broker_names=["localhost:9092"],consumer_group=None,topic="testme")
    assert (len(items) == 1)


def test_produce_to_kafka_with_consumer_group():
    my_obj = TestOject()
    my_obj.id = 10
    with_action(my_obj, action=Action.Added)
    produce_with_action(broker_names=["localhost:9092"],topic="testme",data_item=json.dumps( {'hi' :'there'}   ), id=my_obj.id )
    items = consume(broker_names=["localhost:9092"],consumer_group='test',topic="testme")
    assert (len(items) == 1)


def test_produce_to_kafka_with_consumer_group_2():
    us = user_settings()
    us.userId = 1
    us.preferred_currency = "EUR"
    with_action(us, action=Action.Added)
    print(jsonpickle.encode(us))
    produce_with_action(broker_names=["localhost:9092"],topic="us1",data_item=jsonpickle.encode(us), id=us.userId )
    items = consume(broker_names=["localhost:9092"],consumer_group=None,topic="us")
    print(items[0])
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
    with_action(t, action=Action.Added)
    print(jsonpickle.encode(t))
    produce_with_action(broker_names=["localhost:9092"],topic="t",data_item=jsonpickle.encode(t), id=t.user_id )
    items = consume(broker_names=["localhost:9092"],consumer_group=None,topic="t")
    assert (len(items) == 1)
