import time

from playwright.sync_api import expect

from components.add_to_cart_modal import AddToCartModal
from pages.main_page import FeaturesItems, NavMenu
from utils.markers import shopping_modal, ui, xfail


@ui
@xfail(reason="https://github.com/gwojacek/qa-demo-repository/issues/13")
@shopping_modal
def test_modal_overlay_click_closes_modal(page_on_address):
    """
    [UX BUG] Add-to-cart modal cannot be closed by clicking outside popup.
    """
    features = FeaturesItems(page_on_address)
    features.add_to_cart_by_hover(0, close_modal=False)
    modal = AddToCartModal(page_on_address)
    modal.wait_until_visible()
    NavMenu(page_on_address).home_btn.click()
    modal.wait_until_invisible()
    expect(NavMenu(page_on_address).home_btn).to_be_enabled(timeout=5000)


@ui
@xfail(reason="https://github.com/gwojacek/qa-demo-repository/issues/16")
@shopping_modal
def test_visibility_time_modal(page_on_address):
    """Ensure the add-to-cart modal appears almost instantly."""
    features = FeaturesItems(page_on_address)
    features.card(0).hover()
    expect(features.product_overlay.nth(0)).to_be_visible()
    start = time.perf_counter()
    features.add_to_cart_btn.nth(0).click()
    AddToCartModal(page_on_address).wait_until_visible()
    elapsed = time.perf_counter() - start
    assert elapsed < 0.3, f"Modal took {elapsed:.2f}s to appear"
