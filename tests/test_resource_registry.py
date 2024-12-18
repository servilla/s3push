#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_resource_registry

:Synopsis:
    Pytest for test_resource_registry

:Author:
    servilla

:Created:
    12/17/24
"""
from sqlalchemy import func
from sqlalchemy.orm import Session

import s3push.model.resource_registry as rr


host = "localhost"


def test_engine():
    engine = rr.get_pasta_db_engine(host=host)
    assert engine


def test_session_query():
    engine = rr.get_pasta_db_engine(host=host)
    with Session(engine) as session:
        resources = session.query(rr.ResourceRegistry).order_by(func.random()).limit(10)
        for resource in resources:
            assert resource