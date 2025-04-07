import pytest

from utils.dict_utils import dict_multi_by_key


class FakeClass:
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


@pytest.mark.parametrize(
    ("items", "key", "expected"),
    [
        ([], "id", {}),
        ([FakeClass(1, 2), FakeClass(3, 4)], "non_existent_attribute", {}),
        ([FakeClass(1, 2)], "attr1", {1: [FakeClass(1, 2)]}),
        (
            [FakeClass(1, 2), FakeClass(1, 4)],
            "attr1",
            {1: [FakeClass(1, 2), FakeClass(1, 4)]},
        ),
        (
            [FakeClass(1, 2), FakeClass(2, 4)],
            "attr1",
            {1: [FakeClass(1, 2)], 2: [FakeClass(2, 4)]},
        ),
        (
            [FakeClass(1, 2), FakeClass(1, 3), FakeClass(2, 5)],
            "attr1",
            {1: [FakeClass(1, 2), FakeClass(1, 3)], 2: [FakeClass(2, 5)]},
        ),
        (
            [FakeClass(1, 2), FakeClass(1, 3), FakeClass(2, 5), FakeClass(2, 6)],
            "attr1",
            {
                1: [FakeClass(1, 2), FakeClass(1, 3)],
                2: [FakeClass(2, 5), FakeClass(2, 6)],
            },
        ),
    ],
)
def test_dict_multi_by_key(items, key, expected):
    result = dict_multi_by_key(items, key)
    assert {k: [(i.attr1, i.attr2) for i in v] for k, v in result.items()} == {
        k: [(i.attr1, i.attr2) for i in v] for k, v in expected.items()
    }
