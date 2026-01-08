import os

from playwright.sync_api import Page, expect

from pages.main_page import NavMenu


class DeleteAccountPage:
    def __init__(self, page: Page):
        self.page = page
        self.account_deleted_header = page.locator('h2[data-qa="account-deleted"]')
        self.continue_btn = page.locator('a[data-qa="continue-button"]')

    def delete_account_and_continue(self, click=True):
        # Click 'Delete Account' in nav
        NavMenu(self.page).delete_account_btn.click()
        # Wait for URL to be correct
        expect(self.page).to_have_url("https://www.automationexercise.com/delete_account")
        # Assert the header is present and correct
        expect(self.account_deleted_header).to_be_visible()
        expect(self.account_deleted_header).to_have_text("Account Deleted!")
        if click:
            self.continue_btn.click()
            # Wait for redirect to home
            expect(self.page).to_have_url(os.environ.get("ADDRESS") + "/")
