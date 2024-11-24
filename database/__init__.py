from __future__ import annotations

from typing import ClassVar

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from sqlalchemy_serializer import SerializerMixin

from config import config


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


engine = create_engine(config.SQLALCHEMY_DATABASE_URI)  # type: ignore[attr-defined]
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class CRUDMixin(SerializerMixin):
    __table_args__: ClassVar = {"extend_existing": True}

    def __repr__(self) -> str:
        fields = getattr(self, "__repr_fields__", ())
        fields = ("id", *fields)
        extra = [f"{key}={getattr(self, key, None)}" for key in fields]
        return f"<{self.__class__.__name__}({', '.join(extra)})>"
