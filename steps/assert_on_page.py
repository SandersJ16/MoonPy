#!/usr/bin/env python

from core.sophia_validator import SophiaValidator

class AssertOnPage(SophiaValidator):
    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def valid(self, driver):
        return self.driver.current_url.lower() == self.url.lower()
