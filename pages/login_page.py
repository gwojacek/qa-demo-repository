from playwright.sync_api import Page, expect

from components.consent_popup import ConsentPopup
from pages.main_page import NavMenu


class LoginPage:
    URL = "https://www.automationexercise.com/login"

    def __init__(self, page: Page):
        self.page = page
        # Login form (left)
        self.email_input = page.locator('input[data-qa="login-email"]')
        self.password_input = page.locator('input[data-qa="login-password"]')
        self.login_button = page.locator('button[data-qa="login-button"]')
        self.login_form = page.locator('form[action="/login"]')

        # Signup form (right)
        self.signup_name_input = page.locator('input[data-qa="signup-name"]')
        self.signup_email_input = page.locator('input[data-qa="signup-email"]')
        self.signup_button = page.locator('button[data-qa="signup-button"]')
        self.signup_form = page.locator('form[action="/signup"]')

    def load(self):
        self.page.goto(self.URL)
        ConsentPopup(self.page).accept()  # Handles the popup if present
        expect(self.email_input).to_be_visible()

    def login(self, email, password):
        """Fill login form and submit."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        self.is_logged_in()

    def signup(self, name, email):
        """Fill signup form and submit."""
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()

    def is_logged_in(self):
        nav_menu = NavMenu(self.page)
        expect(nav_menu.logout_btn).to_be_visible(timeout=5000)
        expect(nav_menu.delete_account_btn).to_be_visible(timeout=5000)
        expect(self.page).to_have_url("https://www.automationexercise.com/")

    def not_logged_in(self):
        """Return True if neither Logout nor Delete Account button is displayed."""
        nav_menu = NavMenu(self.page)
        return not (
            nav_menu.logout_btn.is_visible() or nav_menu.delete_account_btn.is_visible()
        )

    def logout(self):
        NavMenu(self.page).logout_btn.click()
        expect(self.page).to_have_url(self.URL)
