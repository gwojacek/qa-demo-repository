from selenium.webdriver.common.by import By

from utils.expected_conditions import EC


class ProductDetailsPage:
    COMPONENT = (By.CSS_SELECTOR, ".product-information")
    NAME = (By.CSS_SELECTOR, "h2")
    PRICE = (By.CSS_SELECTOR, "span span")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input#quantity")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button.cart")

    MODAL = (By.CSS_SELECTOR, ".modal-content")
    VIEW_CART_IN_MODAL = (By.CSS_SELECTOR, ".modal-content a[href='/view_cart']")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, ".modal-content .close-modal")

    def __init__(self, driver):
        self.driver = driver
        self.component = EC.wait_for_element_visible(driver, self.COMPONENT)

    def get_name(self) -> str:
        return EC.find_element(self.component, self.NAME).text.strip()

    def get_price(self) -> int:
        price_text = EC.find_element(self.component, self.PRICE).text.strip()
        return int(price_text.replace("Rs.", "").replace(",", "").strip())

    def _get_info_field(self, label: str) -> str:
        """Return info value from <p> like 'Availability', 'Condition', 'Brand', 'Category'."""
        p_tags = self.component.find_elements(By.CSS_SELECTOR, "p")
        for p in p_tags:
            if label in p.text:
                # e.g. "Condition: New" -> "New"
                return p.text.split(":", 1)[-1].strip()
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
        EC.fill_element(self.component, self.QUANTITY_INPUT, str(qty), clear_first=True)
        return int(
            EC.find_element(self.component, self.QUANTITY_INPUT).get_attribute("value")
        )

    def fill_input_with_characters(self, qty):
        EC.fill_element(self.component, self.QUANTITY_INPUT, str(qty), clear_first=True)
        return EC.find_element(self.component, self.QUANTITY_INPUT).get_attribute(
            "value"
        )

    def get_quantity(self) -> int:
        return int(
            EC.find_element(self.component, self.QUANTITY_INPUT).get_attribute("value")
        )

    def add_to_cart(self, close_modal=True):
        EC.click_element(self.component, self.ADD_TO_CART_BTN)
        EC.wait_for_element_visible(self.driver, self.MODAL)
        if close_modal:
            EC.click_element(self.driver, self.CLOSE_MODAL_BTN)

    def add_to_cart_and_view_cart(self):
        EC.click_element(self.component, self.ADD_TO_CART_BTN)
        EC.wait_for_element_visible(self.driver, self.MODAL)
        EC.click_element(self.driver, self.VIEW_CART_IN_MODAL)
