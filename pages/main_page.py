from playwright.sync_api import Page, expect

from components.add_to_cart_modal import AddToCartModal


class MainPage:
    URL = "https://en.wikipedia.org/wiki/Main_Page"

    def __init__(self, page: Page):
        self.page = page

    def load(self):
        self.page.goto(self.URL)

    def get_title(self):
        return self.page.title()

    def search_input_exists(self):
        return self.page.locator('[name="search"]').is_visible()


class NavMenu:
    def __init__(self, page: Page):
        self.page = page
        self.home_btn = page.locator('[class*="shop-menu"] a[href="/"]')
        self.products_btn = page.locator('[class*="shop-menu"] a[href="/products"]')
        self.cart_btn = page.locator('[class*="shop-menu"] a[href="/view_cart"]')
        self.login_btn = page.locator('[class*="shop-menu"] a[href="/login"]')
        self.logout_btn = page.locator('[class*="shop-menu"] a[href="/logout"]')
        self.contact_btn = page.locator('[class*="shop-menu"] a[href="/contact_us"]')
        self.test_cases_btn = page.locator(
            '[class*="shop-menu"] a[href="/test_cases"]'
        )
        self.api_testing_btn = page.locator('[class*="shop-menu"] a[href="/api_list"]')
        self.video_tutorials_btn = page.locator(
            '[class*="shop-menu"] a[href="/video_tutorials"]'
        )
        self.download_app_btn = page.locator(
            '[class*="shop-menu"] a[href="/download_app"]'
        )
        self.delete_account_btn = page.locator(
            '[class*="shop-menu"] a[href="/delete_account"]'
        )


class FeaturesItems:
    def __init__(self, page: Page):
        self.page = page
        self.component = page.locator(".features_items")
        self.product_cards = self.component.locator(".product-image-wrapper")
        self.view_product_btn = self.product_cards.locator(
            ".choose a[href*='product_details']"
        )
        self.add_to_cart_btn = self.product_cards.locator(
            ".overlay-content .add-to-cart"
        )
        self.product_name = self.product_cards.locator("p")
        self.product_price = self.product_cards.locator("h2")
        self.product_overlay = self.product_cards.locator(".overlay-content")

    def cards(self):
        """Return all product cards as a list of locators."""
        return self.product_cards.all()

    def card(self, index=0):
        """Return a specific product card by index."""
        return self.product_cards.nth(index)

    def view_product(self, index=0):
        self.view_product_btn.nth(index).click()

    def add_to_cart_by_hover(self, index, close_modal=True):
        self.card(index).hover()
        expect(self.product_overlay.nth(index)).to_be_visible()
        self.add_to_cart_btn.nth(index).click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        if close_modal:
            modal.click_continue_shopping()
            modal.wait_until_invisible()
            self.page.wait_for_load_state("networkidle")

    def add_to_cart_and_view_cart(self, index=0):
        self.card(index).hover()
        expect(self.product_overlay.nth(index)).to_be_visible()
        self.add_to_cart_btn.nth(index).click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        modal.click_view_cart()

    def get_product_name(self, index=0):
        return self.product_name.nth(index).inner_text().strip()

    def get_product_detail_url(self, index=0):
        return self.view_product_btn.nth(index).get_attribute("href")

    def get_product_price(self, index=0):
        """
        Returns product price as int, stripping 'Rs. ' and commas.
        Example: "Rs. 1,000" -> 1000
        """
        price_text = self.product_price.nth(index).inner_text()
        # Remove currency and commas, keep only digits
        price = price_text.replace("Rs. ", "").replace(",", "").strip()
        return int(price)
