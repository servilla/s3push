#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    __init__

:Synopsis:

:Author:
    servilla

:Created:
    12/17/24
"""
import logging
from pathlib import Path
import sys

import daiquiri


cwd = Path("../tests").resolve().as_posix()
logfile = cwd + "/tests.log"
daiquiri.setup(level=logging.DEBUG,
               outputs=(daiquiri.output.File(logfile), "stdout",))
logger = daiquiri.getLogger(__name__)

sys.path.insert(0, Path("../src").resolve().as_posix())
