DATE_FORMAT = '%Y-%m-%d'
from kafkaHelper import to_json_with_action, Action


class TestOject():
    def __init__(self):
        self.id = 1
        self.descr = "hi"


def test_to_json():
    my_obj = TestOject()
    to_json_with_action(my_obj, action=Action.Added)
    assert (my_obj.action, Action.Added)
