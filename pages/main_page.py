from selenium.webdriver.common.by import By

from components.modal_shopping import AddToCartModal
from utils.expected_conditions import EC


class MainPage:
    URL = "https://en.wikipedia.org/wiki/Main_Page"

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    def get_title(self):
        return self.driver.title

    def search_input_exists(self):
        return self.driver.find_element("name", "search") is not None


class NavMenu:
    HOME_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/"]')
    PRODUCTS_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/products"]')
    CART_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/view_cart"]')
    LOGIN_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/login"]')
    LOGOUT_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/logout"]')
    CONTACT_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/contact_us"]')
    TEST_CASES_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/test_cases"]')
    API_TESTING_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/api_list"]')
    VIDEO_TUTORIALS_BTN = (
        By.CSS_SELECTOR,
        '[class*="shop-menu"] a[href="/video_tutorials"]',
    )
    DOWNLOAD_APP_BTN = (By.CSS_SELECTOR, '[class*="shop-menu"] a[href="/download_app"]')
    DELETE_ACCOUNT_BTN = (
        By.CSS_SELECTOR,
        '[class*="shop-menu"] a[href="/delete_account"]',
    )

    def click_nav_btn(driver, locator):
        """
        Click any navigation menu button.
        Usage: click_nav_btn(driver, NavMenu.LOGIN_BTN)
        """
        EC.click_element(driver, locator)


class FeaturesItems:
    SECTION = (By.CSS_SELECTOR, ".features_items")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-image-wrapper")
    VIEW_PRODUCT_BTN = (By.CSS_SELECTOR, ".choose a[href*='product_details']")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".overlay-content .add-to-cart")
    PRODUCT_NAME = (By.CSS_SELECTOR, "p")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "h2")
    PRODUCT_OVERLAY = (By.CSS_SELECTOR, ".overlay-content")

    def __init__(self, driver):
        self.driver = driver
        self.component = EC.wait_for_element_visible(driver, self.SECTION)

    def cards(self):
        """Return all product cards as a list."""
        return EC.find_elements(self.component, self.PRODUCT_CARDS)

    def card(self, index=0):
        """Return a specific product card by index."""
        return self.cards()[index]

    def view_product(self, index=0):
        EC.find_element(self.card(index), self.VIEW_PRODUCT_BTN).click()

    def add_to_cart_by_hover(self, index, close_modal=True):
        EC.move_to_element(
            self.driver,
            locator=self.PRODUCT_CARDS,
            index=index,
            wait_for_after_move=self.PRODUCT_OVERLAY,
        )
        EC.find_element(self.card(index), self.ADD_TO_CART_BTN).click()
        AddToCartModal(self.driver).wait_until_visible()
        if close_modal:
            AddToCartModal(self.driver).click_continue_shopping()

    def add_to_cart_and_view_cart(self, index=0):
        EC.move_to_element(
            self.driver,
            locator=self.PRODUCT_CARDS,
            index=index,
            wait_for_after_move=self.PRODUCT_OVERLAY,
        )
        EC.find_element(self.card(index), self.ADD_TO_CART_BTN).click()
        AddToCartModal(self.driver).wait_until_visible()
        AddToCartModal(self.driver).click_view_cart()

    def get_product_name(self, index=0):
        return EC.find_element(self.card(index), self.PRODUCT_NAME).text.strip()

    def get_product_detail_url(self, index=0):
        return EC.find_element(self.card(index), self.VIEW_PRODUCT_BTN).get_attribute(
            "href"
        )

    def get_product_price(self, index=0):
        """
        Returns product price as int, stripping 'Rs. ' and commas.
        Example: "Rs. 1,000" -> 1000
        """
        price_text = EC.find_element(self.card(index), self.PRODUCT_PRICE).text
        # Remove currency and commas, keep only digits
        price = price_text.replace("Rs. ", "").replace(",", "").strip()
        return int(price)
