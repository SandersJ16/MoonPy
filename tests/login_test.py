#!/usr/bin/env python

from core.sophia_test import SophiaTest

from steps.visit_page import VisitPage
from steps.enter_text import EnterText
from steps.hit_enter_with_element_selected import HitEnterWithElementSelected

from validators.element_contains_text import ElementContainsText
from validators.on_page import OnPage


class LoginTestBase(SophiaTest):
    @classmethod
    def required_plugins(cls):
        return set(["auth", "my"])


class LoginTest(LoginTestBase):
    def get_default_steps(self):
        default_steps = super().get_default_steps()
        default_steps["Go To Login Page"] = VisitPage(self.base_url + '/auth/login')
        default_steps["Enter User Name"] = EnterText("justice.longhammer", type="text", name="uname")
        default_steps["Enter Password"] = EnterText("pass1Word", type="password", name="passwd")
        default_steps["Click Login"] = HitEnterWithElementSelected(type="submit", name="login")
        return default_steps

    def validate(self):
        return OnPage(self.base_url + '/my/home')


class BadLoginTest(LoginTestBase):
    def get_default_steps(self):
        default_steps = super().get_default_steps()
        default_steps["Go To Login Page"] = VisitPage(self.base_url + '/auth/login')
        default_steps["Enter User Name"] = EnterText("justin.sanders", type="text", name="uname")
        default_steps["Enter Bad Password"] = EnterText("Fake", type="password", name="passwd")
        default_steps["Click Login"] = HitEnterWithElementSelected(type="submit", name="login")
        return default_steps

    def validate(self):
        return ElementContainsText("The username or password entered is invalid.", id="login-message")
