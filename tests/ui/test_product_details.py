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
            marks=pytest.mark.xfail(reason="accepts mixed string '12abc' as quantity"),
            id="mixed_string",
        ),
        pytest.param("!", id="symbol"),
        pytest.param(
            "-5",
            marks=pytest.mark.xfail(reason="accepts negative numbers"),
            id="negative",
        ),
        pytest.param(
            "3.5",
            marks=pytest.mark.xfail(reason="accepts float as quantity"),
            id="float",
        ),
        pytest.param(
            "  7   ",
            marks=pytest.mark.xfail(reason="accepts padded string as quantity"),
            id="whitespace",
        ),
    ],
)
def test_quantity_non_integer_input_rejected(page_on_address, qty):
    """
    https://github.com/gwojacek/qa-demo-repository/issues/18

    Only positive integers should be allowed.
    Non-integer values must NOT be accepted in the input field.
    """
    features = FeaturesItems(page_on_address)
    features.view_product(0)
    details = ProductDetailsPage(page_on_address)
    val = details.fill_input_with_characters(qty)

    assert (
        isinstance(val, int) and val > 0
    ) or val == "", (
        f"Input '{qty}' should not be accepted as quantity, but got: '{val}'"
    )
