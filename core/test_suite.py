#!/usr/bin/env python

import os
import platform
from collections import OrderedDict
from functools import lru_cache

from core.test_case import TestCase
from tests import *

class TestSuite(object):

    def __init__(self, active_plugins = set()):
        self.active_plugins = set(active_plugins)
        self._tests = None
        self._plugins = None
        self._active_plugins = None
        #print(self.all_tests())


    @property
    def plugins(self):
        if self._plugins is None:
            self._plugins = set()
            for plugin_name in self.active_plugins:
                plugin_class_exists = False
                #TODO
                #Look for plugin class and load it
                if plugin_class_exists:
                    self._plugins.append(plugin_class_exists)
        return self._plugins

    @property
    @lru_cache()
    def tests(self):
        test_classes = [test for test in self.all_tests() if test.required_plugins() <= self.active_plugins and not test.restricted_plugins() & self.active_plugins]
        tests = []
        for TestClass in test_classes:
            test = TestClass()
            for plugin in self.plugins:
                plugin.modTest(test)
            tests.append(test)

        return sorted(tests)


    def all_tests(self):
        return [test for test in self.all_subclasses(TestCase) if test.__name__.endswith("Test")]

    @staticmethod
    def all_subclasses(cls):
        return cls.__subclasses__() + [sub_sub_cls for sub_cls in cls.__subclasses__() for sub_sub_cls in TestSuite.all_subclasses(sub_cls)]

    def run(self):
        test_results = OrderedDict()
        for test in self.tests:
            test_result = test.run(test_results)
            test_results[test.name] = test_result
            print(test_result)

def add_selenium_drivers_to_path():
    system = platform.system()
    is_64_bit = platform.machine().endswith("64")

    current_directory = os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    drivers_path = os.path.join(parent_directory, 'selenium_drivers')
    if system == "Linux" and is_64_bit:
        drivers_path = os.path.join(drivers_path, 'linux64')
    elif system == "Linux" and not is_64_bit:
        drivers_path = os.path.join(drivers_path, 'linux32')
    else:
        raise OSError("Currently this library does not support your system's architecture")

    os.environ["PATH"] += os.pathsep + drivers_path

add_selenium_drivers_to_path()
