from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from utils.expected_conditions import EC


class ConsentPopup:
    CONSENT_BTN = (
        By.CSS_SELECTOR,
        'button[class*="fc-primary-button"][aria-label="Consent"]',
    )

    def __init__(self, driver):
        self.driver = driver

    def accept(self, timeout=5):
        """Click consent if present; ignore if not found."""
        try:
            EC.click_element(self.driver, self.CONSENT_BTN, timeout)
        except TimeoutException:
            pass
