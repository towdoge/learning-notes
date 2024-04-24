# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthUser(Base):
    __tablename__ = "auth_user"
    __table_args__ = {"comment": "test"}

    id = Column(
        INTEGER(11), primary_key=True, unique=True, autoincrement=True, comment="主键id"
    )
    username = Column(VARCHAR(255), comment="username")
    password = Column(VARCHAR(255), comment="password")
