DATE_FORMAT = '%Y-%m-%d'
from kafkaHelper import to_json_with_action, Action, produce_with_action, consume


class TestOject():
    def __init__(self):
        self.id = 1
        self.descr = "hi"


def test_to_json():
    my_obj = TestOject()
    to_json_with_action(my_obj, action=Action.Added)
    assert (my_obj.action, Action.Added)


def test_produce_to_kafka():
    my_obj = TestOject()
    to_json_with_action(my_obj, action=Action.Added)
    produce_with_action(broker_names=["localhost:9092"],topic="testme",data_item=my_obj)
    items = consume(broker_names=["localhost:9092"],consumer_group="testme",topic="testme")
    assert (len(items) == 1)