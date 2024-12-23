#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_push_registry

:Synopsis:
    Pytest for test_push_registry

:Author:
    servilla

:Created:
    12/17/24
"""
from pathlib import Path

from sqlalchemy.orm import Session

import s3push.model.push_registry as pr


CWD = Path(__file__).resolve().parent
PUSH_DB = (CWD / "push_db.sqlite").as_posix()


def _clean_db():
    Path(PUSH_DB).unlink(missing_ok=True)


def test_engine():
    engine = pr._get_push_db_engine(db_path=PUSH_DB)
    assert engine


def test_push_registry_create():
    engine = pr._get_push_db_engine(db_path=PUSH_DB)
    pr.Base.metadata.create_all(engine)
    assert Path(PUSH_DB).exists()
    _clean_db()