"""Utility wrapper around Selenium expected conditions and interactions.

All helpers are grouped in :class:`ExpectedConditions` to keep related waits,
actions, and assertions together while maintaining concise call sites via
class methods.
"""

from typing import Any, List, Optional, Tuple

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as selenium_ec
from selenium.webdriver.support.ui import WebDriverWait


class ExpectedConditions:
    """Collection of reusable Selenium helpers as class methods."""

    default_timeout: int = 3

    # --- Internal utilities -------------------------------------------------
    @classmethod
    def _resolve_timeout(cls, timeout: Optional[int]) -> int:
        return timeout or cls.default_timeout

    # --- Finding elements ---------------------------------------------------
    @staticmethod
    def find_element(driver: WebDriver, locator: Tuple[str, str]) -> WebElement:
        """Return the first matching element.

        Example:
            ExpectedConditions.find_element(driver, LoginLocators.USERNAME_INPUT)
            # where LoginLocators.USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="username"]')
        """

        return driver.find_element(*locator)

    @staticmethod
    def find_elements(driver: WebDriver, locator: Tuple[str, str]) -> List[WebElement]:
        """Return all matching elements.

        Example:
            ExpectedConditions.find_elements(driver, ProductListLocators.ADD_TO_CART_BUTTONS)
            # where ProductListLocators.ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, '.add-to-cart-btn')
        """

        return driver.find_elements(*locator)

    # --- Waits for presence/visibility -------------------------------------
    @classmethod
    def wait_for_element(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> WebElement:
        """Wait for element to be present in DOM."""

        to = cls._resolve_timeout(timeout)
        return WebDriverWait(driver, to).until(
            selenium_ec.presence_of_element_located(locator),
            f"{locator} did not appear in {to} seconds",
        )

    @classmethod
    def wait_for_elements(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> List[WebElement]:
        """Wait for all elements matching locator to be present."""

        to = cls._resolve_timeout(timeout)
        return WebDriverWait(driver, to).until(
            selenium_ec.presence_of_all_elements_located(locator),
            f"{locator} did not appear in {to} seconds",
        )

    @classmethod
    def wait_for_element_visible(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> WebElement:
        """Wait for element to be visible (not just present)."""

        to = cls._resolve_timeout(timeout)
        return WebDriverWait(driver, to).until(
            selenium_ec.visibility_of_element_located(locator),
            f"{locator} is not visible in {to} seconds",
        )

    @classmethod
    def wait_for_elements_visible(
        cls, driver: Any, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> List[WebElement]:
        """Wait for all elements to be visible."""

        to = cls._resolve_timeout(timeout)
        return WebDriverWait(driver, to).until(
            selenium_ec.visibility_of_all_elements_located(locator),
            f"{locator} are not visible in {to} seconds",
        )

    @classmethod
    def wait_for_element_clickable(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> WebElement:
        """Wait for element to be clickable."""

        to = cls._resolve_timeout(timeout)
        return WebDriverWait(driver, to).until(
            selenium_ec.element_to_be_clickable(locator),
            f"{locator} is not clickable in {to} seconds",
        )

    @classmethod
    def wait_for_alert(cls, driver: WebDriver, timeout: Optional[int] = None) -> Any:
        """Wait until a JavaScript alert is present."""

        to = cls._resolve_timeout(timeout)
        return WebDriverWait(driver, to).until(selenium_ec.alert_is_present())

    @classmethod
    def wait_for_element_to_disappear(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> None:
        """Wait until element disappears from DOM."""

        to = cls._resolve_timeout(timeout)
        try:
            WebDriverWait(driver, to).until_not(
                selenium_ec.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element did not disappear within {to} seconds.")

    # --- URL and title checks ----------------------------------------------
    @classmethod
    def wait_until_url_is(
        cls, driver: WebDriver, url: str, timeout: Optional[int] = None
    ) -> None:
        """Wait until current URL is exactly as expected."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.url_to_be(url),
            f"URL did not become {url}, actual: {driver.current_url}",
        )

    @classmethod
    def wait_until_url_contains(
        cls, driver: WebDriver, substring: str, timeout: Optional[int] = None
    ) -> None:
        """Wait until URL contains the given substring."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.url_contains(substring),
            f"URL {driver.current_url} did not contain {substring}",
        )

    @classmethod
    def wait_until_title_is(
        cls, driver: WebDriver, title: str, timeout: Optional[int] = None
    ) -> None:
        """Wait until page title is exactly as expected."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.title_is(title),
            f"Title did not become {title}, actual: {driver.title}",
        )

    @classmethod
    def wait_until_title_contains(
        cls, driver: WebDriver, substring: str, timeout: Optional[int] = None
    ) -> None:
        """Wait until page title contains substring."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.title_contains(substring),
            f"Title {driver.title} did not contain {substring}",
        )

    # --- Text checks --------------------------------------------------------
    @classmethod
    def wait_for_text_in_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait until element contains the given text."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.text_to_be_present_in_element(locator, text),
            f"{locator} did not appear in {to} seconds or {text} did not match",
        )

    @classmethod
    def wait_for_text_not_in_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait until element does NOT contain the given text."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until_not(
            selenium_ec.text_to_be_present_in_element(locator, text),
            f"{locator} did not disappear in {to} seconds or {text} was still present",
        )

    @classmethod
    def wait_for_text_in_element_value(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait until value attribute of element contains the given text."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.text_to_be_present_in_element_value(locator, text),
            f"{locator} did not appear in {to} seconds or {text} did not match",
        )

    # --- Visibility/staleness ----------------------------------------------
    @classmethod
    def wait_for_invisibility(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> None:
        """Wait until element becomes invisible."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.invisibility_of_element_located(locator),
            f"Element {locator} still visible after {to} seconds",
        )

    @classmethod
    def wait_for_staleness_of(
        cls, driver: WebDriver, element: WebElement, timeout: Optional[int] = None
    ) -> None:
        """Wait until element is no longer attached to DOM."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.staleness_of(element),
            f"Element {element} is still attached to the DOM after {to} seconds",
        )

    @classmethod
    def wait_for_frame_to_be_available_and_switch_to_it(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> None:
        """Wait for frame to be available and switch context."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.frame_to_be_available_and_switch_to_it(locator),
            f"Frame {locator} not available in {to} seconds",
        )

    # --- Window handling ----------------------------------------------------
    @classmethod
    def wait_for_new_window_is_opened(
        cls, driver: WebDriver, old_windows: List[str], timeout: Optional[int] = None
    ) -> None:
        """Wait until a new browser window is opened."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.new_window_is_opened(old_windows),
            f"No new window was opened in {to} seconds",
        )

    @classmethod
    def wait_for_number_of_windows_to_be(
        cls, driver: WebDriver, num: int, timeout: Optional[int] = None
    ) -> None:
        """Wait until the number of open windows is as expected."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.number_of_windows_to_be(num),
            f"Number of windows did not become {num} in {to} seconds",
        )

    # --- Selection state ----------------------------------------------------
    @classmethod
    def wait_for_element_located_selection_state_to_be(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        selected: bool,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait until element's selection state matches expected (checkbox/radio)."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.element_located_selection_state_to_be(locator, selected),
            f"Element {locator} selection state did not become {selected} in {to} seconds",
        )

    @classmethod
    def wait_for_element_selection_state_to_be(
        cls,
        driver: WebDriver,
        element: WebElement,
        selected: bool,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait until given element's selection state matches expected."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.element_selection_state_to_be(element, selected),
            f"Element {element} selection state did not become {selected} in {to} seconds",
        )

    @classmethod
    def wait_for_element_to_be_selected(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> None:
        """Wait until element is selected."""

        to = cls._resolve_timeout(timeout)
        WebDriverWait(driver, to).until(
            selenium_ec.element_located_to_be_selected(locator),
            f"Element {locator} was not selected in {to} seconds",
        )

    # --- Actions ------------------------------------------------------------
    @classmethod
    def click_element(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> None:
        """Wait for and click the element."""

        elem = cls.wait_for_element_clickable(driver, locator, timeout)
        elem.click()

    @classmethod
    def click_nth_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        index: int,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait for and click the element at the given index."""

        elems = cls.wait_for_elements(driver, locator, timeout)
        if index >= len(elems):
            raise IndexError(f"No element at index {index} for {locator}")
        elems[index].click()

    @classmethod
    def fill_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        value: str,
        clear_first: bool = True,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait for element, optionally clear, then fill it with value."""

        elem = cls.wait_for_element_visible(driver, locator, timeout)
        if clear_first:
            elem.clear()
        elem.send_keys(value)

    @classmethod
    def fill_nth_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        index: int,
        value: str,
        clear_first: bool = True,
        timeout: Optional[int] = None,
    ) -> None:
        """Wait for all elements, fill the one at given index, optionally clear first."""

        elems = cls.wait_for_elements_visible(driver, locator, timeout)
        if index >= len(elems):
            raise IndexError(f"No element at index {index} for {locator}")
        elem = elems[index]
        if clear_first:
            elem.clear()
        elem.send_keys(value)

    @classmethod
    def clear_element(
        cls, driver: WebDriver, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> None:
        """Wait for an element and clear its value."""

        elem = cls.wait_for_element_visible(driver, locator, timeout)
        elem.clear()

    @classmethod
    def move_to_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        index: int = 0,
        timeout: Optional[int] = None,
        wait_for_after_move: Optional[Tuple[str, str]] = None,
        wait_timeout: Optional[int] = None,
    ) -> None:
        """Move mouse to element at index (default 0).

        Optionally wait for a given sub-element (e.g. overlay) to be visible after hover.
        """

        elems = cls.wait_for_elements(driver, locator, timeout)
        if index >= len(elems):
            raise IndexError(f"No element at index {index} for {locator}")
        target_elem = elems[index]
        ActionChains(driver).move_to_element(target_elem).perform()

        if wait_for_after_move:
            cls.wait_for_elements_visible(
                target_elem, wait_for_after_move, wait_timeout
            )

    @staticmethod
    def drag_and_drop(
        driver: WebDriver, source: WebElement, target: WebElement
    ) -> None:
        """Drag and drop from source to target."""

        ActionChains(driver).drag_and_drop(source, target).perform()

    # --- Attribute/text utilities ------------------------------------------
    @classmethod
    def get_element_attribute(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        attribute: str,
        timeout: Optional[int] = None,
    ) -> str:
        """Wait for element, then return the value of an attribute."""

        elem = cls.wait_for_element(driver, locator, timeout)
        return elem.get_attribute(attribute)

    @classmethod
    def get_nth_element_attribute(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        attribute: str,
        index: int,
        timeout: Optional[int] = None,
    ) -> str:
        """Wait for all elements, get attribute of element at index."""

        elems = cls.wait_for_elements(driver, locator, timeout)
        if index >= len(elems):
            raise IndexError(f"No element at index {index} for {locator}")
        return elems[index].get_attribute(attribute)

    @staticmethod
    def get_texts_from_elements(
        elements: List[WebElement], read_hidden: bool = False
    ) -> List[str]:
        """Return texts from list of elements, optionally including hidden text."""

        if read_hidden:
            return [elem.get_attribute("textContent") for elem in elements]
        return [elem.text for elem in elements]

    # --- Display/visibility checks -----------------------------------------
    @staticmethod
    def is_displayed(driver: WebDriver, locator: Tuple[str, str]) -> bool:
        """Check if element is displayed (returns False if not found)."""

        try:
            return driver.find_element(*locator).is_displayed()
        except NoSuchElementException:
            return False

    # --- Text presence checks ----------------------------------------------
    @classmethod
    def check_text_in_nth_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        text: str,
        index: int = 0,
        timeout: Optional[int] = None,
    ) -> bool:
        """Return True if text is present in element at given index."""

        elems = cls.wait_for_elements(driver, locator, timeout)
        if index >= len(elems):
            raise IndexError(f"No element at index {index} for {locator}")
        return text in elems[index].text

    @classmethod
    def check_text_not_in_nth_element(
        cls,
        driver: WebDriver,
        locator: Tuple[str, str],
        text: str,
        index: int = 0,
        timeout: Optional[int] = None,
    ) -> bool:
        """Return True if text is NOT present in element at given index."""

        elems = cls.wait_for_elements(driver, locator, timeout)
        if index >= len(elems):
            raise IndexError(f"No element at index {index} for {locator}")
        return text not in elems[index].text


EC = ExpectedConditions
