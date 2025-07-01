from selenium.webdriver.common.by import By

from utils.expected_conditions import (click_element, wait_for_element_visible,
                                       wait_for_invisibility)


class AddToCartModalLocators:
    MODAL = (By.CSS_SELECTOR, ".modal-content")
    VIEW_CART_BTN = (By.CSS_SELECTOR, ".modal-content a[href='/view_cart']")
    CONTINUE_SHOPPING_BTN = (
        By.CSS_SELECTOR,
        'button.btn.btn-success.close-modal.btn-block[data-dismiss="modal"]',
    )


class AddToCartModal:
    def __init__(self, driver):
        self.driver = driver

    def wait_until_visible(self, timeout=5):
        """Wait for modal to be visible."""
        return wait_for_element_visible(
            self.driver, AddToCartModalLocators.MODAL, timeout
        )

    def click_continue_shopping(self, timeout=3):
        """Click 'Continue Shopping' button on modal."""
        click_element(
            self.driver, AddToCartModalLocators.CONTINUE_SHOPPING_BTN, timeout
        )

    def click_view_cart(self, timeout=3):
        """Click 'View Cart' link in modal."""
        click_element(self.driver, AddToCartModalLocators.VIEW_CART_BTN, timeout)

    def wait_until_invisible(self, timeout=5):
        """Wait for modal to be visible."""
        return wait_for_invisibility(self.driver, AddToCartModalLocators.MODAL, timeout)
