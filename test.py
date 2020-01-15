#!/usr/bin/env python

from core.sophia_test import SophiaTest
from tests import *

if __name__ == "__main__":
    for cls in SophiaTest.__subclasses__():
        print(cls.__name__)
