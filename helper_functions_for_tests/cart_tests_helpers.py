import os
from dataclasses import dataclass

from playwright.sync_api import Page

from pages.cart import CartPage
from pages.main_page import FeaturesItems, NavMenu
from pages.product_details_page import ProductDetailsPage


@dataclass
class ProductInfo:
    name: str
    price: int
    idx: int = 0
    qty: int = 1


def add_from_main(page: Page, idx=0, close_modal=True) -> ProductInfo:
    """
    Add a product from main page (FeaturesItems) and return its info.
    """
    features = FeaturesItems(page)
    prod_name = features.get_product_name(idx)
    price = features.get_product_price(idx)
    features.add_to_cart_by_hover(index=idx, close_modal=close_modal)
    return ProductInfo(name=prod_name, price=price, idx=idx, qty=1)


def add_from_details(
    page: Page, idx=0, qty=1, close_modal=True, back_to_main=False
) -> ProductInfo:
    """
    Add product from details page with given quantity, return its info.
    """
    features = FeaturesItems(page)
    features.view_product(idx)
    details = ProductDetailsPage(page)
    details.set_quantity(qty)
    prod_name = details.get_name()
    price = details.get_price()
    details.add_to_cart(close_modal=close_modal)
    if back_to_main:
        page.goto(os.environ.get("ADDRESS"))
    return ProductInfo(name=prod_name, price=price, idx=idx, qty=qty)


def open_cart(page: Page) -> CartPage:
    NavMenu(page).cart_btn.click()
    return CartPage(page)


# Assertions


def norm(string):
    """Normalize whitespaces for better name comparison."""
    return " ".join(str(string).split())


def assert_cart_row_names(cart: CartPage, expected_names):
    rows = cart.get_all_rows()
    cart_names = {norm(r.name()) for r in rows}
    for name in expected_names:
        assert norm(name) in cart_names, f"Product {name} not found in cart"


def assert_cart_row_quantities(cart: CartPage, products):
    rows = cart.get_all_rows()
    for name, qty in products:
        row = next((r for r in rows if norm(r.name()) == norm(name)), None)
        assert row, f"Product {name} not found in cart"
        assert (
            row.quantity() == qty
        ), f"Expected quantity {qty} for {name}, got {row.quantity()}"


def assert_cart_row_prices(cart: CartPage, products):
    rows = cart.get_all_rows()
    for name, _, price in products:
        row = next((r for r in rows if norm(r.name()) == norm(name)), None)
        assert row, f"Product {name} not found in cart"
        assert (
            row.price() == price
        ), f"Expected price {price} for {name}, got {row.price()}"


def assert_cart_row_line_totals(cart: CartPage, products):
    rows = cart.get_all_rows()
    for name, qty, price in products:
        row = next((r for r in rows if norm(r.name()) == norm(name)), None)
        assert row, f"Product {name} not found in cart"
        expected_line_total = qty * price
        assert (
            row.total() == expected_line_total
        ), f"Line total mismatch for {name}: {row.total()} != {price} * {qty}"


def assert_cart_total(cart: CartPage, products):
    expected_total = sum(qty * price for (_, qty, price) in products)
    actual_total = cart.get_total_cart_value()
    assert (
        actual_total == expected_total
    ), f"Cart total mismatch: {actual_total} != {expected_total}"


def assert_cart_all(cart: CartPage, products):
    """
    products: list of (name, qty, price)
    """
    assert_cart_row_names(cart, [name for name, _, _ in products])
    assert_cart_row_quantities(cart, [(name, qty) for name, qty, _ in products])
    assert_cart_row_prices(cart, products)
    assert_cart_row_line_totals(cart, products)
    assert_cart_total(cart, products)
