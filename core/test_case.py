#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
from collections import OrderedDict
from selenium import webdriver

from core.test_step import TestStepError

class TestCase(with_metaclass(ABCMeta, object)):
    dependencies = []

    @classmethod
    def required_plugins(cls):
        return set()

    @classmethod
    def restricted_plugins(cls):
        return set()

    def __init__(self, config=OrderedDict(), driver=webdriver.Chrome):
        self.driver = driver()
        self.steps = self.get_default_steps()

    @property
    def name(self):
        return self.__class__.__name__


    @abstractmethod
    def get_default_steps(self):
        return OrderedDict()


    def setup(self):
        pass


    def execute_steps(self):
        for step_name, step in self.steps.items():
            try:
                step.execute(self.driver)
            except Exception as e:
                raise TestStepError("Failed during step {step_name} with Error: {exception}".format(step_name=step_name, exception=e))


    def cleanup(self):
        self.driver.quit()


    def run(self, previous_test_results={}):
        result = self.TestResult(self)

        for dependency in self.dependencies:
            if not previous_test_results[dependency.name]["passed"]:
                result.skipped = True
                result.failed_dependencies.append(dependency.name)

        if not result.skipped:
            result.passed = False
            try:
                self.setup()
            except Exception as e:
                result.exception = e
                result.exception_step = "Setup"
            else:
                try:
                    self.execute_steps()
                except TestStepError as e:
                    result.exception = e
                    result.exception_step = "Execute"

                finally:
                    try:
                        self.cleanup()
                    except Exception as e:
                        # If we already have an exception don't override it,
                        # there is a good chance this Exception is a side effect
                        # of the first one. This means the first Exception is
                        # more relevant.
                        if result.exception is None:
                            result.exception = e
                            result.exception_step = "Cleanup"
        return result


    def __lt__(self, other):
        if self in other.dependencies:
            return True

        if self.__class__ in other.dependencies:
            return True

        for dependency in other.dependencies:
            if self < dependency:
                return True

        return False


    def __gt__(self, other):
        if other in self.dependencies:
            return True

        if other.__class__ in self.dependencies:
            return True

        for dependency in self.dependencies:
            if self > dependency:
                return True

        return False


    def __eq__(self, other):
        return not self > other and not self < other


    class TestResult(object):
        def __init__(self, test):
            self.test = test
            self.name = self.test.name
            self.skipped = False

            self.failed_dependencies = []
            self.passed = None
            self.exception = None
            self.exception_step = None

        def __str__(self):
            if self.exception is not None:
                return 'Test {name} Failed with Exception: {exception} during the {exception_step} step'.format(**self.__dict__)

            elif self.skipped:
                return 'Test {name} was skipped because dependencies {failed_dependencies} either failed or were skipped'.format(**self.__dict__)

            elif not self.passed:
                return 'Test {name} Failed!'.format(**self.__dict__)
            else:
                return 'Test {name} Passed!'.format(**self.__dict__)

        def __repr__(self):
            return "TestResult(%s)" % self.name
