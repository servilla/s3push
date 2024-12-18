#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    resource_registry

:Synopsis:

:Author:
    servilla

:Created:
    12/17/24
"""
import urllib.parse

import daiquiri
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import DeclarativeBase

from s3push.config import Config


logger = daiquiri.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class ResourceRegistry(Base):
    __tablename__ = "resource_registry"
    __table_args__ = {"schema": "datapackagemanager"}

    resource_id = Column(String, primary_key=True)
    package_id = Column(String)
    resource_type = Column(String)
    resource_location = Column(String)
    resource_size = Column(Integer)
    md5_checksum = Column(String)
    sha1_checksum = Column(String)

def get_pasta_db_engine(host: str):
    db = (
        Config.DB_DRIVER
        + "://"
        + Config.DB_USER
        + ":"
        + urllib.parse.quote_plus(Config.DB_PW)
        + "@"
        + host
        + ":"
        + Config.DB_PORT
        + "/"
        + Config.DB_DB
    )

    engine = create_engine(db)
    return engine