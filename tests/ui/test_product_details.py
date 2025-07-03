import pytest

from pages.main_page import FeaturesItems
from pages.product_details_page import ProductDetailsPage
from utils.markers import product_details, ui


@ui
@product_details
@pytest.mark.parametrize(
    "qty",
    [
        pytest.param("abc", id="letters"),
        pytest.param(
            "12abc",
            marks=pytest.mark.xfail(
                reason="BUG no. 7: accepts mixed string '12abc' as quantity"
            ),
            id="mixed_string",
        ),
        pytest.param("!", id="symbol"),
        pytest.param(
            "-5",
            marks=pytest.mark.xfail(reason="BUG no. 7: accepts negative numbers"),
            id="negative",
        ),
        pytest.param(
            "3.5",
            marks=pytest.mark.xfail(reason="BUG no. 7: accepts float as quantity"),
            id="float",
        ),
        pytest.param(
            "  7   ",
            marks=pytest.mark.xfail(reason="BUG no. 7: accepts padded string as quantity"),
            id="whitespace",
        ),
    ],
)
def test_quantity_non_integer_input_rejected(driver_on_address, qty):
    """
    [BUG/SECURITY] Product quantity field allows invalid input.

    See: BUGS.md section 'Not enough input Restriction on Numeric and Text Fields'

    Only positive integers should be allowed.
    Non-integer values must NOT be accepted in the input field.
    """
    features = FeaturesItems(driver_on_address)
    features.view_product(0)
    details = ProductDetailsPage(driver_on_address)
    val = details.fill_input_with_characters(qty)

    assert (
        isinstance(val, int) and val > 0
    ) or val == "", (
        f"Input '{qty}' should not be accepted as quantity, but got: '{val}'"
    )
