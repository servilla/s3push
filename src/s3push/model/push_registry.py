#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    push_registry

:Synopsis:

:Author:
    servilla

:Created:
    12/17/24
"""
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase

from s3push.config import Config
import daiquiri

logger = daiquiri.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class PushRegistry(Base):
    __tablename__ = "push_registry"

    resource_id = Column(String, primary_key=True)
    package_id = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_location = Column(String, nullable=False)
    resource_size = Column(Integer, nullable=True)
    md5_checksum = Column(String, nullable=True)
    sha1_checksum = Column(String, nullable=True)
    date_created = Column(DateTime, nullable=False)
    date_pushed = Column(DateTime, nullable=True)


def get_push_db_engine(db_path: str = Config.PUSH_DB):
    engine = create_engine("sqlite:///" + db_path)
    return engine