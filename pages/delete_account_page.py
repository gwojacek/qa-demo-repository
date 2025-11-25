import os

from selenium.webdriver.common.by import By

from pages.main_page import NavMenu
from utils.basefunctions import BaseFunctions
from utils.expected_conditions import EC


class DeleteAccountPage(BaseFunctions):
    ACCOUNT_DELETED_HEADER = (By.CSS_SELECTOR, 'h2[data-qa="account-deleted"]')
    CONTINUE_BTN = (By.CSS_SELECTOR, 'a[data-qa="continue-button"]')

    def delete_account_and_continue(self, click=True):
        # Click 'Delete Account' in nav
        NavMenu.click_nav_btn(self.driver, NavMenu.DELETE_ACCOUNT_BTN)
        # Wait for URL to be correct
        EC.wait_until_url_is(
            self.driver, "https://www.automationexercise.com/delete_account"
        )
        # Assert the header is present and correct
        elem = EC.wait_for_element_visible(
            self.driver, DeleteAccountPage.ACCOUNT_DELETED_HEADER
        )
        assert "ACCOUNT DELETED!" == elem.text
        if click:
            EC.click_element(self.driver, DeleteAccountPage.CONTINUE_BTN)
            # Wait for redirect to home
            EC.wait_until_url_is(self.driver, os.environ.get("ADDRESS"))
