import time

from components.modal_shopping import AddToCartModal
from pages.main_page import FeaturesItems, NavMenu
from utils.expected_conditions import (
    find_element,
    move_to_element,
    wait_for_element_clickable,
)
from utils.markers import shopping_modal, ui, xfail


@ui
@xfail(reason="https://github.com/gwojacek/qa-demo-repository/issues/13")
@shopping_modal
def test_modal_overlay_click_closes_modal(driver_on_address):
    """
    [UX BUG] Add-to-cart modal cannot be closed by clicking outside popup.
    """
    features = FeaturesItems(driver_on_address)
    features.add_to_cart_by_hover(0, close_modal=False)
    AddToCartModal(driver_on_address).wait_until_visible()
    NavMenu.click_nav_btn(driver_on_address, NavMenu.HOME_BTN)
    AddToCartModal(driver_on_address).wait_until_invisible()
    wait_for_element_clickable(driver_on_address, NavMenu.HOME_BTN, timeout=5)


@ui
@xfail(reason="https://github.com/gwojacek/qa-demo-repository/issues/16")
@shopping_modal
def test_visibility_time_modal(driver_on_address):
    """Ensure the add-to-cart modal appears almost instantly."""
    features = FeaturesItems(driver_on_address)
    move_to_element(
        driver_on_address,
        FeaturesItems.PRODUCT_CARDS,
        index=0,
        wait_for_after_move=FeaturesItems.PRODUCT_OVERLAY,
    )
    start = time.perf_counter()
    find_element(features.card(0), FeaturesItems.ADD_TO_CART_BTN).click()
    AddToCartModal(driver_on_address).wait_until_visible()
    elapsed = time.perf_counter() - start
    assert elapsed < 0.3, f"Modal took {elapsed:.2f}s to appear"
