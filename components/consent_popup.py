from playwright.sync_api import Page, TimeoutError


class ConsentPopup:
    def __init__(self, page: Page):
        self.page = page
        self.consent_btn = page.locator(
            'button[class*="fc-primary-button"][aria-label="Consent"]'
        )

    def accept(self, timeout=5000):
        """Click consent if present; ignore if not found."""
        try:
            self.consent_btn.click(timeout=timeout)
        except TimeoutError:
            pass
