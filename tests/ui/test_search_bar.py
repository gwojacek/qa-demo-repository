import time

import pytest

from pages.main_page import MainPage


@pytest.mark.ui
def test_wikipedia_main_page(driver):
    page = MainPage(driver)
    page.load()
    assert "Wikipedia" in page.get_title()


@pytest.mark.ui
def test_wikipedia_main_page_failed(driver):
    page = MainPage(driver)
    page.load()
    assert "Wikipedia" not in page.get_title()


@pytest.mark.ui
def test_wikipedia_main_page2(driver):
    page = MainPage(driver)
    page.load()
    assert "Wikipedia" in page.get_title()


@pytest.mark.ui
def test_wikipedia_main_page_failed2(driver):
    page = MainPage(driver)
    page.load()
    assert "Wikipedia" not in page.get_title()
