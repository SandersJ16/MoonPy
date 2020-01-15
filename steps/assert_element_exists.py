#!/usr/bin/env python

from core.sophia_validator import SophiaValidator
from util.single_element_matcher import SingleElementMatcher, NoElementMatchFoundError

class ElementExists(SophiaValidator, SingleElementMatcher):
    def valid(self, driver):
        try:
            self._getElement(driver)
            return True
        except NoElementMatchFoundError:
            return False
