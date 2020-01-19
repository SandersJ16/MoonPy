#!/usr/bin/env python

from core.test_step import TestStep, TestStepAssertionFail
from util.single_element_matcher import SingleElementMatcher, NoElementMatchFound

class AssertElementContainsText(TestStep, SingleElementMatcher):
    def __init__(self, text, *, case_sensitive=False, **kwargs):
        super().__init__(**kwargs)
        self.case_sensitive = case_sensitive
        self.text = text

    def execute(self, driver):
        element = self._getElement(driver)

        if element.tag_name == 'input' and element.get_attribute('type') in ('text', 'number', 'email', 'url', 'search', 'tel'):
            element_text = element.get_attribute('value')
        else:
            element_text = element.text

        if (not self.case_sensitive and element_text.lower() != self.text.lower()) or element_text != self.text:
            raise TestStepAssertionFail("Element did not contain expected text: Expected '{}' but found '{}' (Case {})".format(self.text,
                                                                                                                             element_text,
                                                                                                                             "Sensitive" if self.case_sensitive else "Insentive"))
