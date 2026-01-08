from playwright.sync_api import Page, expect


class AddToCartModal:
    def __init__(self, page: Page):
        self.page = page
        self.modal = page.locator(".modal-content")
        self.view_cart_btn = self.modal.locator('a[href="/view_cart"]')
        self.continue_shopping_btn = self.modal.locator(
            'button.btn.btn-success.close-modal.btn-block[data-dismiss="modal"]'
        )

    def wait_until_visible(self, timeout=5000):
        """Wait for modal to be visible."""
        expect(self.modal).to_be_visible(timeout=timeout)

    def click_continue_shopping(self):
        """Click 'Continue Shopping' button on modal."""
        self.continue_shopping_btn.click()

    def click_view_cart(self):
        """Click 'View Cart' link in modal."""
        self.view_cart_btn.click()

    def wait_until_invisible(self, timeout=5000):
        """Wait for modal to be invisible."""
        expect(self.modal).to_be_hidden(timeout=timeout)
