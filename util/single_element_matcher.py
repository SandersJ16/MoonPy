#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
from selenium.webdriver.common.by import By

class SingleElementMatcher(with_metaclass(ABCMeta, object)):
    valid_search_criteria = ["id", "name", "title", "tag", "type", "data_testing_id", "xpath", "css"]

    def __init__(self, *args, **kwargs):
        self.search_criteria = {}
        for key in self.valid_search_criteria:
            value = kwargs.pop(key, None)
            if value is not None:
                self.search_criteria[self._clean_attribute(key)] = value

        super().__init__(*args, **kwargs)


    def _getElement(self, driver):
        for attribute, value  in self.search_criteria.items():
            find_type, search_value = self._get_values(attribute, value)

            elements = driver.find_elements(find_type, search_value)

            for element in elements:
                try:
                    self._valid_element(element)
                except NoElementMatchFound:
                    pass
                else:
                    return element
            if elements:
                raise NoElementMatchFound("No Matching Element Found")
        raise NoElementMatchFound("No Matching Element Found")



    def _valid_element(self, element):
        error_messages = []

        for attribute, value  in self.search_criteria.items():
            if attribute in ("id", "name", "title", "type", "data_testing_id") and element.get_attribute(attribute) != value:
                error_messages.append("Element is missing attribute {0}='{1}'".format(attribute, value))
            elif attribute is "tag" and element.tag_name.lower() != str(value).lower():
                error_messages.append("Element is wrong tag type, got tag {0} but was expecting {0}".format(element.tag_name.lower(), str(value).lower()))
            elif attribute is "xpath":
                xpath_elements = driver.find_elements_by_xpath(value)
                if element not in xpath_elements:
                    error_messages.append("Element didn't match XPath " + value)
            elif attribute is "css":
                xpath_elements = driver.find_elements_by_css_selector(value)
                if element not in xpath_elements:
                    error_messages.append("Element didn't match CSS " + value)

        if error_messages:
            raise NoElementMatchFound("Element was invalid because: " + ", ".join(error_messages))
        return True

    def _get_values(self, attribute, value):
        if attribute is "id":
            find_type, search_value = By.ID, value
        elif attribute is "name":
            find_type, search_value = By.NAME, value
        elif attribute is "xpath":
            find_type, search_value = By.XPATH, value
        elif attribute is "css":
            find_type, search_value = By.CSS_SELECTOR, value
        elif attribute is "tag":
            find_type, search_value = By.TAG_NAME, value
        elif attribute in ("title", "type", "data_testing_id"):
            find_type, search_value = By.XPATH, "//*[@{attribute}='{value}']".format(attribute=attribute, value=value)
        else :
            find_type, search_value = By.ID, value

        return find_type, search_value


    def _clean_attribute(self, attribute):
        return attribute.replace("_", "-")

class NoElementMatchFound(Exception):
    pass
