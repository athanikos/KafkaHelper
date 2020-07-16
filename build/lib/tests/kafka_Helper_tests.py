import json

DATE_FORMAT = '%Y-%m-%d'
from kafkaHelper.kafkaHelper import with_action, Action, produce_with_action, consume


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
