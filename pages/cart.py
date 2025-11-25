from dataclasses import dataclass
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement

from utils.expected_conditions import EC


@dataclass
class ProductRow:
    row_element: WebElement

    # Locators for use with find_element (no asterisks)
    NAME = (By.CSS_SELECTOR, ".cart_description h4 a")
    CATEGORY = (By.CSS_SELECTOR, ".cart_description p")
    PRICE = (By.CSS_SELECTOR, ".cart_price p")
    QUANTITY = (By.CSS_SELECTOR, ".cart_quantity button")
    TOTAL = (By.CSS_SELECTOR, ".cart_total_price")
    DELETE_BTN = (By.CSS_SELECTOR, ".cart_quantity_delete")

    def name(self) -> str:
        return EC.find_element(self.row_element, self.NAME).text.strip()

    def category(self) -> str:
        return EC.find_element(self.row_element, self.CATEGORY).text.strip()

    def price(self) -> int:
        txt = EC.find_element(self.row_element, self.PRICE).text
        return int(txt.replace("Rs. ", "").replace(",", "").strip())

    def quantity(self) -> int:
        txt = EC.find_element(self.row_element, self.QUANTITY).text.strip()
        return int(txt)

    def total(self) -> int:
        txt = EC.find_element(self.row_element, self.TOTAL).text
        return int(txt.replace("Rs. ", "").replace(",", "").strip())

    def delete(self):
        EC.find_element(self.row_element, self.DELETE_BTN).click()

    def id(self) -> int:
        return int(self.row_element.get_attribute("id").replace("product-", ""))

    # todo wont work, there need to be fixed bug/make an improvement (bug no 3 in bugs.md)
    def set_quantity(self, value: int):
        """
        Set the quantity in the cart's input field for this product row.
        """
        input_elem = EC.find_element(
            self.row_element, (By.CSS_SELECTOR, "input[type='number'], input")
        )
        input_elem.clear()
        input_elem.send_keys(str(value))


@dataclass
class CartPage:
    driver: WebDriver

    TABLE = (By.CSS_SELECTOR, "table.table.table-condensed")
    ROWS = (By.CSS_SELECTOR, "tr[id^='product-']")

    def _table(self) -> WebElement:
        return EC.find_element(self.driver, self.TABLE)

    def _rows(self) -> list[WebElement]:
        return EC.find_elements(self._table(), self.ROWS)

    def get_product_row(self, product_id: int) -> ProductRow:
        row = EC.find_element(
            self._table(), (By.CSS_SELECTOR, f"tr#product-{product_id}")
        )
        return ProductRow(row)

    def get_all_rows(self) -> list[ProductRow]:
        return [ProductRow(row) for row in self._rows()]

    def get_product_ids(self) -> list[int]:
        return [row.id() for row in self.get_all_rows()]

    def assert_all_line_totals(self):
        for row in self.get_all_rows():
            assert (
                row.total() == row.price() * row.quantity()
            ), f"Line total mismatch for id={row.id()}: {row.total()} != {row.price()} * {row.quantity()}"

    def get_total_cart_value(self) -> int:
        return sum(row.total() for row in self.get_all_rows())
