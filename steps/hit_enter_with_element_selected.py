#!/usr/bin/env python

from selenium.webdriver.common.keys import Keys

from core.test_step import TestStep
from util.single_element_matcher import SingleElementMatcher

class HitEnterWithElementSelected(TestStep, SingleElementMatcher):

    def execute(self, driver):
        element = self._getElement(driver)
        element.send_keys(Keys.RETURN)

