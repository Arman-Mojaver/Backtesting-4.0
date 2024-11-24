If one day you want to add indexes to a table, you can do it as follows:
__table_args__ = (
    Index("ix_raw_point_d1_instrument", "instrument"),
)

And in the test you can check the content of RawPointD1.__table__.indexes.
Maybe create a helper function for the test.
