#!/usr/bin/env python

from core.test_case import TestCase

from steps.visit_page import VisitPage
from steps.enter_text import EnterText
from steps.assert_element_contains_text import AssertElementContainsText
from steps.hit_enter_with_element_selected import HitEnterWithElementSelected

class BingSearchTest(TestCase):
    def get_default_steps(self):
        default_steps = super().get_default_steps()
        default_steps["Go To Bing.com"] = VisitPage("https://bing.com")
        default_steps["Enter 'Korn Bah' in search field"] = EnterText("Korn Bah", type="search", name="q")
        default_steps["Hit Enter key in search field"] = HitEnterWithElementSelected(type="search", name="q")
        default_steps["Assert Form contains text 'Korn Bah'"] = AssertElementContainsText("Korn Bah", id="sb_form_q")
        return default_steps
