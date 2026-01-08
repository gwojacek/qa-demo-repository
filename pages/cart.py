from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass
class ProductRow:
    row_locator: Locator

    @property
    def name_locator(self) -> Locator:
        return self.row_locator.locator(".cart_description h4 a")

    @property
    def category_locator(self) -> Locator:
        return self.row_locator.locator(".cart_description p")

    @property
    def price_locator(self) -> Locator:
        return self.row_locator.locator(".cart_price p")

    @property
    def quantity_locator(self) -> Locator:
        return self.row_locator.locator(".cart_quantity button")

    @property
    def total_locator(self) -> Locator:
        return self.row_locator.locator(".cart_total_price")

    @property
    def delete_btn_locator(self) -> Locator:
        return self.row_locator.locator(".cart_quantity_delete")

    def name(self) -> str:
        return self.name_locator.inner_text().strip()

    def category(self) -> str:
        return self.category_locator.inner_text().strip()

    def price(self) -> int:
        txt = self.price_locator.inner_text()
        return int(txt.replace("Rs. ", "").replace(",", "").strip())

    def quantity(self) -> int:
        txt = self.quantity_locator.inner_text().strip()
        return int(txt)

    def total(self) -> int:
        txt = self.total_locator.inner_text()
        return int(txt.replace("Rs. ", "").replace(",", "").strip())

    def delete(self):
        self.delete_btn_locator.click()

    def id(self) -> int:
        return int(self.row_locator.get_attribute("id").replace("product-", ""))

    def set_quantity(self, value: int):
        """
        Set the quantity in the cart's input field for this product row.
        """
        input_elem = self.row_locator.locator("input[type='number'], input")
        input_elem.fill(str(value))


@dataclass
class CartPage:
    page: Page

    @property
    def table_locator(self) -> Locator:
        return self.page.locator("table.table.table-condensed")

    @property
    def rows_locator(self) -> Locator:
        return self.table_locator.locator("tr[id^='product-']")

    def get_product_row(self, product_id: int) -> ProductRow:
        row_locator = self.table_locator.locator(f"tr#product-{product_id}")
        return ProductRow(row_locator)

    def get_all_rows(self) -> list[ProductRow]:
        return [ProductRow(row) for row in self.rows_locator.all()]

    def get_product_ids(self) -> list[int]:
        return [row.id() for row in self.get_all_rows()]

    def assert_all_line_totals(self):
        for row in self.get_all_rows():
            assert (
                row.total() == row.price() * row.quantity()
            ), f"Line total mismatch for id={row.id()}: {row.total()} != {row.price()} * {row.quantity()}"

    def get_total_cart_value(self) -> int:
        return sum(row.total() for row in self.get_all_rows())
