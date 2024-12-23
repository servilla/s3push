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
from datetime import datetime

from sqlalchemy import create_engine, Engine, Column, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Session

from s3push.config import Config
import daiquiri


logger = daiquiri.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class ResourceRegistry(Base):
    __tablename__ = "resource_registry"

    resource_id = Column(String, primary_key=True)
    package_id = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_location = Column(String, nullable=False)
    resource_size = Column(Integer, nullable=True)
    md5_checksum = Column(String, nullable=True)
    sha1_checksum = Column(String, nullable=True)
    date_created = Column(DateTime, nullable=False)
    date_pushed = Column(DateTime, nullable=True)


class PackageRegistry(Base):
    __tablename__ = "package_registry"

    package_id = Column(String, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    date_pushed = Column(DateTime, nullable=True)



def _get_push_db_engine(db_path: str = Config.PUSH_DB) -> Engine:
    engine = create_engine("sqlite:///" + db_path)
    return engine


def set_package(engine: Engine, package_id: str, date_created: datetime) -> None:
    # engine = _get_push_db_engine()
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        package = PackageRegistry()
        package.package_id = package_id
        package.date_created = date_created
        session.add(package)
        session.commit()
