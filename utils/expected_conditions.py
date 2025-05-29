"""
Base Selenium functions for UI automation:
- Locators expected as (By.CSS_SELECTOR, '...'), typically from a locators class.
- Examples show real-world testing scenarios with creative selectors and context.
"""

from typing import Any, List, Optional, Tuple

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

default_timeout = 30


def find_element(driver: WebDriver, locator: Tuple[str, str]) -> WebElement:
    """Return the first matching element.

    Example:
        find_element(driver, LoginLocators.USERNAME_INPUT)
        # where LoginLocators.USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="username"]')
    """
    return driver.find_element(*locator)


def find_elements(driver: WebDriver, locator: Tuple[str, str]) -> List[WebElement]:
    """Return all matching elements.

    Example:
        find_elements(driver, ProductListLocators.ADD_TO_CART_BUTTONS)
        # where ProductListLocators.ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, '.add-to-cart-btn')
    """
    return driver.find_elements(*locator)


def wait_for_element(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> WebElement:
    """Wait for element to be present in DOM.

    Example:
        wait_for_element(driver, MenuLocators.SIDEBAR_TOGGLE)
        # MenuLocators.SIDEBAR_TOGGLE = (By.CSS_SELECTOR, 'button.sidebar-toggle')
    """
    to = timeout or default_timeout
    return WebDriverWait(driver, to).until(
        EC.presence_of_element_located(locator),
        f"{locator} did not appear in {to} seconds",
    )


def wait_for_elements(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> List[WebElement]:
    """Wait for all elements matching locator to be present.

    Example:
        wait_for_elements(driver, CheckoutLocators.STEP_LABELS)
        # CheckoutLocators.STEP_LABELS = (By.CSS_SELECTOR, '.checkout-step-label')
    """
    to = timeout or default_timeout
    return WebDriverWait(driver, to).until(
        EC.presence_of_all_elements_located(locator),
        f"{locator} did not appear in {to} seconds",
    )


def wait_for_element_visible(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> WebElement:
    """Wait for element to be visible (not just present).

    Example:
        wait_for_element_visible(driver, NotificationLocators.SUCCESS_BANNER)
        # NotificationLocators.SUCCESS_BANNER = (By.CSS_SELECTOR, '.alert-success')
    """
    to = timeout or default_timeout
    return WebDriverWait(driver, to).until(
        EC.visibility_of_element_located(locator),
        f"{locator} is not visible in {to} seconds",
    )


def wait_for_elements_visible(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> List[WebElement]:
    """Wait for all elements to be visible.

    Example:
        wait_for_elements_visible(driver, ModalLocators.VISIBLE_OPTIONS)
        # ModalLocators.VISIBLE_OPTIONS = (By.CSS_SELECTOR, '.modal .option:visible')
    """
    to = timeout or default_timeout
    return WebDriverWait(driver, to).until(
        EC.visibility_of_all_elements_located(locator),
        f"{locator} are not visible in {to} seconds",
    )


def wait_for_element_clickable(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> WebElement:
    """Wait for element to be clickable.

    Example:
        wait_for_element_clickable(driver, DashboardLocators.CREATE_TASK_BUTTON)
        # DashboardLocators.CREATE_TASK_BUTTON = (By.CSS_SELECTOR, 'button.create-task')
    """
    to = timeout or default_timeout
    return WebDriverWait(driver, to).until(
        EC.element_to_be_clickable(locator),
        f"{locator} is not clickable in {to} seconds",
    )


def wait_for_alert(driver: WebDriver, timeout: Optional[int] = None) -> Any:
    """Wait until a JavaScript alert is present.

    Example:
        wait_for_alert(driver)
        # After triggering a confirm() popup.
    """
    to = timeout or default_timeout
    return WebDriverWait(driver, to).until(EC.alert_is_present())


def wait_for_element_to_disappear(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> None:
    """Wait until element disappears from DOM.

    Example:
        wait_for_element_to_disappear(driver, LoaderLocators.PAGE_SPINNER)
        # LoaderLocators.PAGE_SPINNER = (By.CSS_SELECTOR, '.spinner')
    """
    to = timeout or default_timeout
    try:
        WebDriverWait(driver, to).until_not(EC.presence_of_element_located(locator))
    except TimeoutException:
        raise TimeoutException(f"Element did not disappear within {to} seconds.")


def wait_until_url_is(
    driver: WebDriver, url: str, timeout: Optional[int] = None
) -> None:
    """Wait until current URL is exactly as expected.

    Example:
        wait_until_url_is(driver, "https://app.example.com/welcome")
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.url_to_be(url), f"URL did not become {url}, actual: {driver.current_url}"
    )


def wait_until_url_contains(
    driver: WebDriver, substring: str, timeout: Optional[int] = None
) -> None:
    """Wait until URL contains the given substring.

    Example:
        wait_until_url_contains(driver, "/settings/profile")
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.url_contains(substring),
        f"URL {driver.current_url} did not contain {substring}",
    )


def wait_until_title_is(
    driver: WebDriver, title: str, timeout: Optional[int] = None
) -> None:
    """Wait until page title is exactly as expected.

    Example:
        wait_until_title_is(driver, "Order Confirmation")
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.title_is(title), f"Title did not become {title}, actual: {driver.title}"
    )


def wait_until_title_contains(
    driver: WebDriver, substring: str, timeout: Optional[int] = None
) -> None:
    """Wait until page title contains substring.

    Example:
        wait_until_title_contains(driver, "Report")
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.title_contains(substring),
        f"Title {driver.title} did not contain {substring}",
    )


def wait_for_text_in_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    text: str,
    timeout: Optional[int] = None,
) -> None:
    """Wait until element contains the given text.

    Example:
        wait_for_text_in_element(driver, ToastLocators.MESSAGE, "Upload complete!")
        # ToastLocators.MESSAGE = (By.CSS_SELECTOR, '.toast-message')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.text_to_be_present_in_element(locator, text),
        f"{locator} did not appear in {to} seconds or {text} did not match",
    )


def wait_for_text_not_in_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    text: str,
    timeout: Optional[int] = None,
) -> None:
    """Wait until element does NOT contain the given text.

    Example:
        wait_for_text_not_in_element(driver, AlertLocators.ERROR, "Critical")
        # AlertLocators.ERROR = (By.CSS_SELECTOR, '.alert-danger')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until_not(
        EC.text_to_be_present_in_element(locator, text),
        f"{locator} did not disappear in {to} seconds or {text} was still present",
    )


def wait_for_text_in_element_value(
    driver: WebDriver,
    locator: Tuple[str, str],
    text: str,
    timeout: Optional[int] = None,
) -> None:
    """Wait until value attribute of element contains the given text.

    Example:
        wait_for_text_in_element_value(driver, FilterLocators.SEARCH_INPUT, "report_2024")
        # FilterLocators.SEARCH_INPUT = (By.CSS_SELECTOR, 'input[type="search"]')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.text_to_be_present_in_element_value(locator, text),
        f"{locator} did not appear in {to} seconds or {text} did not match",
    )


def wait_for_invisibility(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> None:
    """Wait until element becomes invisible.

    Example:
        wait_for_invisibility(driver, PopupLocators.BACKDROP)
        # PopupLocators.BACKDROP = (By.CSS_SELECTOR, '.modal-backdrop')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.invisibility_of_element_located(locator),
        f"Element {locator} still visible after {to} seconds",
    )


def wait_for_staleness_of(
    driver: WebDriver, element: WebElement, timeout: Optional[int] = None
) -> None:
    """Wait until element is no longer attached to DOM.

    Example:
        elem = find_element(driver, TableLocators.FIRST_ROW)
        # TableLocators.FIRST_ROW = (By.CSS_SELECTOR, 'tr[data-row="1"]')
        wait_for_staleness_of(driver, elem)
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.staleness_of(element),
        f"Element {element} is still attached to the DOM after {to} seconds",
    )


def wait_for_frame_to_be_available_and_switch_to_it(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> None:
    """Wait for frame to be available and switch context.

    Example:
        wait_for_frame_to_be_available_and_switch_to_it(driver, ReportLocators.IFRAME)
        # ReportLocators.IFRAME = (By.CSS_SELECTOR, 'iframe#report-frame')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.frame_to_be_available_and_switch_to_it(locator),
        f"Frame {locator} not available in {to} seconds",
    )


def wait_for_new_window_is_opened(
    driver: WebDriver, old_windows: List[str], timeout: Optional[int] = None
) -> None:
    """Wait until a new browser window is opened.

    Example:
        old_windows = driver.window_handles
        driver.find_element(*LinkLocators.EXPORT_PDF).click()
        wait_for_new_window_is_opened(driver, old_windows)
        # LinkLocators.EXPORT_PDF = (By.CSS_SELECTOR, 'a.export-pdf')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.new_window_is_opened(old_windows),
        f"No new window was opened in {to} seconds",
    )


def wait_for_number_of_windows_to_be(
    driver: WebDriver, num: int, timeout: Optional[int] = None
) -> None:
    """Wait until the number of open windows is as expected.

    Example:
        wait_for_number_of_windows_to_be(driver, 2)
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.number_of_windows_to_be(num),
        f"Number of windows did not become {num} in {to} seconds",
    )


def wait_for_element_located_selection_state_to_be(
    driver: WebDriver,
    locator: Tuple[str, str],
    selected: bool,
    timeout: Optional[int] = None,
) -> None:
    """Wait until element's selection state matches expected (checkbox/radio).

    Example:
        wait_for_element_located_selection_state_to_be(driver, PreferencesLocators.EMAIL_OPT_IN, True)
        # PreferencesLocators.EMAIL_OPT_IN = (By.CSS_SELECTOR, 'input[type="checkbox"][name="email-opt-in"]')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.element_located_selection_state_to_be(locator, selected),
        f"Element {locator} selection state did not become {selected} in {to} seconds",
    )


def wait_for_element_selection_state_to_be(
    driver: WebDriver,
    element: WebElement,
    selected: bool,
    timeout: Optional[int] = None,
) -> None:
    """Wait until given element's selection state matches expected.

    Example:
        checkbox = find_element(driver, PreferencesLocators.EMAIL_OPT_IN)
        wait_for_element_selection_state_to_be(driver, checkbox, False)
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.element_selection_state_to_be(element, selected),
        f"Element {element} selection state did not become {selected} in {to} seconds",
    )


def wait_for_element_to_be_selected(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> None:
    """Wait until element is selected.

    Example:
        wait_for_element_to_be_selected(driver, FilterLocators.YEAR_OPTION_2024)
        # FilterLocators.YEAR_OPTION_2024 = (By.CSS_SELECTOR, 'option[value="2024"]')
    """
    to = timeout or default_timeout
    WebDriverWait(driver, to).until(
        EC.element_located_to_be_selected(locator),
        f"Element {locator} was not selected in {to} seconds",
    )


# ===================== ACTIONS =====================


def click_element(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> None:
    """Wait for and click the element.

    Example:
        click_element(driver, ProductListLocators.ADD_TO_CART)
        # ProductListLocators.ADD_TO_CART = (By.CSS_SELECTOR, '.add-to-cart-btn')
    """
    elem = wait_for_element_clickable(driver, locator, timeout)
    elem.click()


def click_nth_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    index: int,
    timeout: Optional[int] = None,
) -> None:
    """Wait for and click the element at the given index.

    Example:
        click_nth_element(driver, GalleryLocators.IMAGE_THUMBNAIL, 4)
        # GalleryLocators.IMAGE_THUMBNAIL = (By.CSS_SELECTOR, '.gallery-thumb')
    """
    elems = wait_for_elements(driver, locator, timeout)
    if index >= len(elems):
        raise IndexError(f"No element at index {index} for {locator}")
    elems[index].click()


def fill_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    value: str,
    clear_first: bool = True,
    timeout: Optional[int] = None,
) -> None:
    """Wait for element, optionally clear, then fill it with value.

    Example:
        fill_element(driver, AccountFormLocators.USERNAME, "cooluser123")
        # AccountFormLocators.USERNAME = (By.CSS_SELECTOR, 'input#username')
    """
    elem = wait_for_element_visible(driver, locator, timeout)
    if clear_first:
        elem.clear()
    elem.send_keys(value)


def fill_nth_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    index: int,
    value: str,
    clear_first: bool = True,
    timeout: Optional[int] = None,
) -> None:
    """Wait for all elements, fill the one at given index, optionally clear first.

    Example:
        fill_nth_element(driver, SurveyLocators.OPTION_INPUTS, 2, "Other")
        # SurveyLocators.OPTION_INPUTS = (By.CSS_SELECTOR, '.survey-option input')
    """
    elems = wait_for_elements_visible(driver, locator, timeout)
    if index >= len(elems):
        raise IndexError(f"No element at index {index} for {locator}")
    elem = elems[index]
    if clear_first:
        elem.clear()
    elem.send_keys(value)


def clear_element(
    driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
) -> None:
    """Wait for an element and clear its value.

    Example:
        clear_element(driver, SearchLocators.SEARCH_FIELD)
        # SearchLocators.SEARCH_FIELD = (By.CSS_SELECTOR, 'input[type="search"]')
    """
    elem = wait_for_element_visible(driver, locator, timeout)
    elem.clear()


def move_to_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    index: int = 0,
    timeout: Optional[int] = None,
) -> None:
    """Move mouse to element at index (default 0).

    Example:
        move_to_element(driver, NavLocators.MENU_ITEMS, 3)
        # NavLocators.MENU_ITEMS = (By.CSS_SELECTOR, 'nav .menu-item')
    """
    elems = wait_for_elements_visible(driver, locator, timeout)
    if index >= len(elems):
        raise IndexError(f"No element at index {index} for {locator}")
    ActionChains(driver).move_to_element(elems[index]).perform()


def drag_and_drop(driver: WebDriver, source: WebElement, target: WebElement) -> None:
    """Drag and drop from source to target.

    Example:
        drag_and_drop(driver, card_elem, column_elem)
        # Where card_elem, column_elem are WebElement objects from a kanban board.
    """
    ActionChains(driver).drag_and_drop(source, target).perform()


# ===================== ATTRIBUTE/TEXT UTILS =====================


def get_element_attribute(
    driver: WebDriver,
    locator: Tuple[str, str],
    attribute: str,
    timeout: Optional[int] = None,
) -> str:
    """Wait for element, then return the value of an attribute.

    Example:
        get_element_attribute(driver, ProfileLocators.AVATAR, "src")
        # ProfileLocators.AVATAR = (By.CSS_SELECTOR, 'img.profile-avatar')
    """
    elem = wait_for_element(driver, locator, timeout)
    return elem.get_attribute(attribute)


def get_nth_element_attribute(
    driver: WebDriver,
    locator: Tuple[str, str],
    attribute: str,
    index: int,
    timeout: Optional[int] = None,
) -> str:
    """Wait for all elements, get attribute of element at index.

    Example:
        get_nth_element_attribute(driver, ListLocators.ITEM_LINKS, "href", 0)
        # ListLocators.ITEM_LINKS = (By.CSS_SELECTOR, '.item-list a')
    """
    elems = wait_for_elements(driver, locator, timeout)
    if index >= len(elems):
        raise IndexError(f"No element at index {index} for {locator}")
    return elems[index].get_attribute(attribute)


def get_texts_from_elements(
    elements: List[WebElement], read_hidden: bool = False
) -> List[str]:
    """Return texts from list of elements, optionally including hidden text.

    Example:
        get_texts_from_elements(driver.find_elements(*DropdownLocators.OPTIONS))
        # DropdownLocators.OPTIONS = (By.CSS_SELECTOR, '.dropdown-item')
    """
    if read_hidden:
        return [elem.get_attribute("textContent") for elem in elements]
    return [elem.text for elem in elements]


# ===================== DISPLAY/VISIBILITY CHECKS =====================


def is_displayed(driver: WebDriver, locator: Tuple[str, str]) -> bool:
    """Check if element is displayed (returns False if not found).

    Example:
        is_displayed(driver, TooltipLocators.HELP_TOOLTIP)
        # TooltipLocators.HELP_TOOLTIP = (By.CSS_SELECTOR, '.tooltip-help')
    """
    try:
        return driver.find_element(*locator).is_displayed()
    except NoSuchElementException:
        return False


# ===================== TEXT CHECKS =====================


def check_text_in_nth_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    text: str,
    index: int = 0,
    timeout: Optional[int] = None,
) -> bool:
    """Return True if text is present in element at given index.

    Example:
        check_text_in_nth_element(driver, NotificationLocators.MESSAGE_TEXTS, "Success", 1)
        # NotificationLocators.MESSAGE_TEXTS = (By.CSS_SELECTOR, '.notification .msg')
    """
    elems = wait_for_elements(driver, locator, timeout)
    if index >= len(elems):
        raise IndexError(f"No element at index {index} for {locator}")
    return text in elems[index].text


def check_text_not_in_nth_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    text: str,
    index: int = 0,
    timeout: Optional[int] = None,
) -> bool:
    """Return True if text is NOT present in element at given index.

    Example:
        check_text_not_in_nth_element(driver, TabLocators.TAB_LABELS, "Inactive", 2)
        # TabLocators.TAB_LABELS = (By.CSS_SELECTOR, '.tab-label')
    """
    elems = wait_for_elements(driver, locator, timeout)
    if index >= len(elems):
        raise IndexError(f"No element at index {index} for {locator}")
    return text not in elems[index].text
