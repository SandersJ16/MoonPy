#!/usr/bin/env python

from core.test_step import TestStep
from util.single_element_matcher import SingleElementMatcher

class EnterText(TestStep, SingleElementMatcher):

    def __init__(self, text, *, clear=True, **kwargs):
        self.text = text
        self.clear = clear
        super().__init__(**kwargs)


    def execute(self, driver):
        element = self._getElement(driver)
        if self.clear:
            element.clear()

        element.send_keys(self.text)



    def __repr__(self):
        representation = "EnterText('" + self.text + "'"
        for attribute, value in self.search_criteria.items():
            representation += ", " + attribute + "='" + value + "'"
        if not self.clear:
            representation += ", clear=False"
        representation += ")"
        return representation



