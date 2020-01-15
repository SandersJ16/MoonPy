#!/usr/bin/env python

from core.sophia_test_suite import SophiaTestSuite

if __name__ == "__main__":
    s = SophiaTestSuite("wellspring", "dev")
    s.run()
