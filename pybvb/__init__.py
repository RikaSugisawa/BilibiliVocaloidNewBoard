#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pybvb.util import *
logging.basicConfig()

try:
    import pkg_resources
    __version__ = pkg_resources.working_set.require("pybvb")[0].version
except:
    pass
