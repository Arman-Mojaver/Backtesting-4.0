from database import CRUDMixin


def test_repr():
    class FakeModel(CRUDMixin):
        __repr_fields__ = ("attr1",)

        def __init__(self, attr1):
            self.attr1 = attr1

    assert repr(FakeModel(attr1="some_value")) == "<FakeModel(id=None, attr1=some_value)>"
