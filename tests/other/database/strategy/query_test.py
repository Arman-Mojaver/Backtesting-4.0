from database.models import Strategy
from testing_utils.set_utils import set_of_tuples


def test_all_with_empty_table():
    assert Strategy.query.all() == []


def test_all_with_table_items(other_strategies):
    assert set_of_tuples(Strategy.query.all()) == set_of_tuples(other_strategies)
