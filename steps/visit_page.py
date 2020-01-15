#!/usr/bin/env python

from core.test_step import TestStep

class VisitPage(TestStep):

    def __init__(self, url):
        self.url = url

    def execute(self, driver):
        driver.get(self.url)

