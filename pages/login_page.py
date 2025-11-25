from selenium.webdriver.common.by import By

from components.consent_popup import ConsentPopup
from pages.main_page import NavMenu
from utils.basefunctions import BaseFunctions
from utils.expected_conditions import EC


class LoginPage(BaseFunctions):
    URL = "https://www.automationexercise.com/login"

    # --- Locators ---
    # Login form (left)
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[data-qa="login-email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[data-qa="login-password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[data-qa="login-button"]')
    LOGIN_FORM = (By.CSS_SELECTOR, 'form[action="/login"]')

    # Signup form (right)
    SIGNUP_NAME_INPUT = (By.CSS_SELECTOR, 'input[data-qa="signup-name"]')
    SIGNUP_EMAIL_INPUT = (By.CSS_SELECTOR, 'input[data-qa="signup-email"]')
    SIGNUP_BUTTON = (By.CSS_SELECTOR, 'button[data-qa="signup-button"]')
    SIGNUP_FORM = (By.CSS_SELECTOR, 'form[action="/signup"]')

    def load(self):
        self.driver.get(self.URL)
        ConsentPopup(self.driver).accept()  # Handles the popup if present
        EC.wait_for_element(self.driver, self.EMAIL_INPUT)

    def login(self, email, password):
        """Fill login form and submit."""
        EC.fill_element(self.driver, self.EMAIL_INPUT, email)
        EC.fill_element(self.driver, self.PASSWORD_INPUT, password)
        EC.click_element(self.driver, self.LOGIN_BUTTON)
        self.is_logged_in()

    def signup(self, name, email):
        """Fill signup form and submit."""
        EC.fill_element(self.driver, self.SIGNUP_NAME_INPUT, name)
        EC.fill_element(self.driver, self.SIGNUP_EMAIL_INPUT, email)
        EC.click_element(self.driver, self.SIGNUP_BUTTON)

    def is_logged_in(self):
        EC.wait_for_element_clickable(self.driver, NavMenu.LOGOUT_BTN, timeout=5)
        EC.wait_for_element_clickable(self.driver, NavMenu.DELETE_ACCOUNT_BTN, timeout=5)
        assert (
            self.current_url().rstrip("/") == "https://www.automationexercise.com"
        ), f"Unexpected URL: {self.current_url()}"

    def not_logged_in(self):
        """Return True if neither Logout nor Delete Account button is displayed."""
        return not (
            EC.is_displayed(self.driver, NavMenu.LOGOUT_BTN)
            or EC.is_displayed(self.driver, NavMenu.DELETE_ACCOUNT_BTN)
        )

    def logout(self):
        NavMenu.click_nav_btn(self.driver, NavMenu.LOGOUT_BTN)
        assert self.current_url() == self.URL, f"Unexpected URL: {self.current_url()}"
