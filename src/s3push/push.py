#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    push

:Synopsis:

:Author:
    servilla

:Created:
    12/17/24
"""
import logging
from pathlib import Path
import sys

import click
import daiquiri


CWD = Path(".").resolve().as_posix()
LOGFILE = CWD + "/push.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.File(LOGFILE),
        "stdout",
    ),
)
logger = daiquiri.getLogger(__name__)


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.group(context_settings=CONTEXT_SETTINGS)
def push():
    pass

@push.command(context_settings=CONTEXT_SETTINGS)
@click.argument("host", type=str)
def bootstrap(host: str):
    print(host)

if __name__ == "__main__":
    push()