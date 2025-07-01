from components.modal_shopping import AddToCartModal
from pages.main_page import FeaturesItems, NavMenu
from utils.expected_conditions import wait_for_element_clickable
from utils.markers import shopping_modal, ui, xfail


@ui
@xfail(reason="BUG no. 2")
@shopping_modal
def test_modal_overlay_click_closes_modal(driver_on_address):
    """
    [UX BUG] Add-to-cart modal cannot be closed by clicking outside popup.
    See: BUGS.md section 'Modal Blocks UI and Cannot Be Closed by Clicking Outside'
    """
    features = FeaturesItems(driver_on_address)
    features.add_to_cart_by_hover(0, close_modal=False)
    AddToCartModal(driver_on_address).wait_until_visible()
    NavMenu.click_nav_btn(driver_on_address, NavMenu.HOME_BTN)
    AddToCartModal(driver_on_address).wait_until_invisible()
    wait_for_element_clickable(driver_on_address, NavMenu.HOME_BTN, timeout=5)
