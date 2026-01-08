from playwright.sync_api import Page, Locator

from components.add_to_cart_modal import AddToCartModal


class ProductDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.component = page.locator(".product-information")
        self.name_locator = self.component.locator("h2")
        self.price_locator = self.component.locator("span span")
        self.quantity_input = self.component.locator("input#quantity")
        self.add_to_cart_btn = self.component.locator("button.cart")

    def get_name(self) -> str:
        return self.name_locator.inner_text().strip()

    def get_price(self) -> int:
        price_text = self.price_locator.inner_text().strip()
        return int(price_text.replace("Rs.", "").replace(",", "").strip())

    def _get_info_field(self, label: str) -> str:
        """Return info value from <p> like 'Availability', 'Condition', 'Brand', 'Category'."""
        p_tags = self.component.locator("p").all()
        for p in p_tags:
            if label in p.inner_text():
                # e.g. "Condition: New" -> "New"
                return p.inner_text().split(":", 1)[-1].strip()
        return ""

    def get_category(self) -> str:
        return self._get_info_field("Category")

    def get_availability(self) -> str:
        return self._get_info_field("Availability")

    def get_condition(self) -> str:
        return self._get_info_field("Condition")

    def get_brand(self) -> str:
        return self._get_info_field("Brand")

    def set_quantity(self, qty: int) -> int:
        self.quantity_input.fill(str(qty))
        return int(self.quantity_input.input_value())

    def fill_input_with_characters(self, qty):
        self.quantity_input.clear()
        self.quantity_input.press_sequentially(str(qty))
        return self.quantity_input.input_value()

    def get_quantity(self) -> int:
        return int(self.quantity_input.input_value())

    def add_to_cart(self, close_modal=True):
        self.add_to_cart_btn.click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        if close_modal:
            modal.click_continue_shopping()

    def add_to_cart_and_view_cart(self):
        self.add_to_cart_btn.click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        modal.click_view_cart()
