from utils.hash_utils import make_hashable


def test_make_hashable_dict():
    input_dict = {"b": 2, "a": 1, "c": 3}
    result = make_hashable(input_dict)
    expected = (("a", 1), ("b", 2), ("c", 3))
    assert result == expected


def test_make_hashable_nested_dict():
    input_dict = {"x": {"b": 2, "a": 1}, "y": {"d": 4, "c": 3}}
    result = make_hashable(input_dict)
    expected = (("x", (("a", 1), ("b", 2))), ("y", (("c", 3), ("d", 4))))
    assert result == expected


def test_make_hashable_list():
    input_list = [3, 1, 2]
    result = make_hashable(input_list)
    expected = (3, 1, 2)
    assert result == expected


def test_make_hashable_nested_list():
    input_list = [3, [1, 2], [4, [5, 6]]]
    result = make_hashable(input_list)
    expected = (3, (1, 2), (4, (5, 6)))
    assert result == expected


def test_make_hashable_mixed_structures():
    input_value = {
        "list": [3, 1, 2],
        "dict": {"b": [2, 1], "a": {"x": 1}},
        "set": {1, 2, 3},
        "tuple": (10, 20, 30),
    }
    result = make_hashable(input_value)
    expected = (
        ("dict", (("a", (("x", 1),)), ("b", (2, 1)))),
        ("list", (3, 1, 2)),
        ("set", (1, 2, 3)),
        ("tuple", (10, 20, 30)),
    )
    assert result == expected


def test_make_hashable_scalar_values():
    assert make_hashable(42) == 42
    assert make_hashable("hello") == "hello"
    assert make_hashable(3.14) == 3.14
    assert make_hashable(None) is None
    assert make_hashable(True) is True  # noqa: FBT003
    assert make_hashable(False) is False  # noqa: FBT003
