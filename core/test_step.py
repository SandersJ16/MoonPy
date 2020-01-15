#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class TestStep(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def execute(self, driver):
        pass

class TestStepError(Exception):
    pass

class TestStepAssertionFail(Exception):
    pass
