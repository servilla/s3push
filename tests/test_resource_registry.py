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

import s3push.model.resource_registry as resource_registry


def test_engine():
    engine = resource_registry._get_pasta_db_engine()
    assert engine


def test_data_packages_query():
    data_packages = resource_registry.get_data_packages()
    for data_package in data_packages:
        print(data_package.package_id, data_package.date_created, data_package.resource_type)