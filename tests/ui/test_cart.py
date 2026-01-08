import pytest

from helper_functions_for_tests.cart_tests_helpers import (
    add_from_details,
    add_from_main,
    assert_cart_all,
    open_cart,
)
from utils.markers import cart, ui


@ui
@cart
def test_add_single_product(page_on_address):
    """Add a single product from the main page and verify it appears in the cart."""

    prod = add_from_main(page_on_address, idx=0)
    cart = open_cart(page_on_address)
    assert_cart_all(cart, [(prod.name, prod.qty, prod.price)])


@ui
@cart
@pytest.mark.xfail(reason="Likely application bug causing cart total mismatch")
def test_add_two_products(page_on_address):
    """Add two different products from the main page and verify both are listed."""

    prod1 = add_from_main(page_on_address, idx=0)
    prod2 = add_from_main(page_on_address, idx=1)
    cart = open_cart(page_on_address)
    assert_cart_all(
        cart,
        [
            (prod1.name, prod1.qty, prod1.price),
            (prod2.name, prod2.qty, prod2.price),
        ],
    )


@ui
@cart
def test_add_same_product_main_and_details(page_on_address):
    """
    Add the same product from main page and details page.
    Quantities should sum in cart (not show as two lines).
    """
    # Add from main (qty=1 by default)
    prod_main = add_from_main(page_on_address, idx=0)
    # Add from details (qty=3)
    prod_details = add_from_details(page_on_address, idx=0, qty=3)

    cart = open_cart(page_on_address)

    # Should appear once in cart, with quantity summed
    assert_cart_all(
        cart,
        [
            (prod_main.name, prod_main.qty + prod_details.qty, prod_main.price),
        ],
    )


@ui
@cart
def test_add_different_products_main_and_details(page_on_address):
    """
    Add one product from main and a different one from details.
    Both should be present in cart, each with correct quantity.
    """
    # Add from main (idx=0, qty=1)
    prod1 = add_from_main(page_on_address, idx=0)
    # Add from details (idx=1, qty=2)
    prod2 = add_from_details(page_on_address, idx=1, qty=2)

    cart = open_cart(page_on_address)
    assert_cart_all(
        cart,
        [
            (prod1.name, prod1.qty, prod1.price),
            (prod2.name, prod2.qty, prod2.price),
        ],
    )


@ui
@cart
def test_add_multiple_products_from_details(page_on_address):
    """Add multiple products via the details pages and confirm the cart summary."""

    prod1 = add_from_details(page_on_address, idx=1, qty=2, back_to_main=True)
    prod2 = add_from_details(page_on_address, idx=2, qty=5, back_to_main=True)
    cart = open_cart(page_on_address)
    assert_cart_all(
        cart,
        [(prod1.name, prod1.qty, prod1.price), (prod2.name, prod2.qty, prod2.price)],
    )


@ui
@cart
@pytest.mark.parametrize(
    "qty",
    [
        pytest.param(999, id="three_digit"),
        pytest.param(
            int(1e100),
            marks=pytest.mark.xfail(
                reason="https://github.com/gwojacek/qa-demo-repository/issues/18"
            ),
            id="googol",
        ),
    ],
)
def test_add_massive_quantity(page_on_address, qty):
    """
    - Only up to 3 numeric characters should be accepted.
    - Values with more than 3 digits (like a googol) should be rejected or trimmed by the input field.
    """
    prod = add_from_details(page_on_address, idx=0, qty=qty)
    actual_qty = str(prod.qty)
    assert len(actual_qty) <= 3, (
        f"Input '{qty}' resulted in quantity '{actual_qty}' "
        f"(length {len(actual_qty)}), expected max 3 chars"
    )
    cart = open_cart(page_on_address)
    assert_cart_all(cart, [(prod.name, prod.qty, prod.price)])


@ui
@cart
def test_cart_quantity_editable(page_on_address):
    """
    https://github.com/gwojacek/qa-demo-repository/issues/14

    Currently skipped due to product input field in cart being non-editable.
    """

    pytest.skip(reason="BUG no. 3: Cart Quantity Modification Not Working.")
    # Example for future implementation (once bug is fixed):
    # prod = add_from_main(page_on_address, idx=0)
    # cart = open_cart(page_on_address)
    # row = cart.get_all_rows()[0]
    # row.set_quantity(3)
    # assert row.quantity() == 3
    # assert row.total() == row.price() * 3
    # cart.assert_all_line_totals()


@ui
@cart
def test_cart_product_image_redirects_to_details(page_on_address):
    """
    Currently skipped until feature is implemented.
    """

    pytest.skip(reason="https://github.com/gwojacek/qa-demo-repository/issues/15")

    # Example for future implementation:
    # prod = add_from_main(page_on_address, idx=0)
    # cart = open_cart(page_on_address)
    # row = cart.get_all_rows()[0]
    # image = row.row_locator.locator(".cart_product img")  # Update selector as needed
    # image.click()
    # details = ProductDetailsPage(page_on_address)
    # expect(details.get_name()).to_equal(prod.name)
