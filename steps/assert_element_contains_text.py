#!/usr/bin/env python

from core.test_step import TestStep, TestStepAssertionFail
from util.single_element_matcher import SingleElementMatcher, NoElementMatchFound

class ElementContainsText(TestStep, SingleElementMatcher):
    def __init__(self, text, *, case_sensitive=False, **kwargs):
        super().__init__(**kwargs)
        self.case_sensitive = case_sensitive
        self.text = text

    def execute(self, driver):
        try:
            element = self._getElement(driver)
        except NoElementMatchFound:
            raise TestStepAssertionError("No element matching ")
        else:
            if (not case_sensitive and element.text.lower() != self.text.lower()) or element.text != self.text:
                raise TestStepAssertionFail("")
