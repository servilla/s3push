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
from datetime import datetime
import urllib.parse
from typing import Any

import daiquiri
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Session, Query

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
    date_created = Column(DateTime)

def _get_pasta_db_engine():
    db = (
        Config.DB_DRIVER
        + "://"
        + Config.DB_USER
        + ":"
        + urllib.parse.quote_plus(Config.DB_PW)
        + "@"
        + Config.HOST
        + ":"
        + Config.DB_PORT
        + "/"
        + Config.DB_DB
    )

    engine = create_engine(db)
    return engine


def get_data_packages(start_date: datetime = "2013-01-01T00:00:00Z") -> Query:
    engine = _get_pasta_db_engine()
    with Session(engine) as session:
        resources = (
            session.query(ResourceRegistry)
            .filter(ResourceRegistry.date_created >= start_date)
            .filter(ResourceRegistry.resource_type == "dataPackage")
        )
    return resources
