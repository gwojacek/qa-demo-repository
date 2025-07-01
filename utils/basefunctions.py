import time
from pathlib import Path

from utils.expected_conditions import wait_for_element


class BaseFunctions:
    def __init__(self, driver):
        self.driver = driver

    def go_to(self, url):
        """Navigate to a URL."""
        self.driver.get(url)

    def refresh(self):
        """Refresh current page."""
        self.driver.refresh()

    def current_url(self):
        """Return current page URL."""
        return self.driver.current_url

    def get_title(self):
        """Return current page title."""
        return self.driver.title

    def scroll_to(self, locator, timeout=None):
        """Scroll to an element located by locator (waits for it first)."""
        elem = wait_for_element(self.driver, locator, timeout=timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem
        )

    def switch_to_window(self, index=0):
        """Switch to a browser window by index."""
        handles = self.driver.window_handles
        if index >= len(handles):
            raise IndexError(f"No window at index {index}. Available: {handles}")
        self.driver.switch_to.window(handles[index])

    def close(self):
        """Close current browser window."""
        self.driver.close()

    def take_screenshot(driver, name=""):
        """
        Save a screenshot in tests/artifacts/ with a timestamp and optional name.
        Example: tests/artifacts/test_234010_17_06_2024_after_login.png
        /home/jacek/PycharmProjects/QA_DEMO_REPO/tests/artifacts and click reload from the disc to see the screenshot
        """
        # Safe timestamp for filenames (no colons!)
        ts = time.strftime("%H%M%S_%d_%m_%Y")
        name = f"_{name}" if name else ""
        file_name = f"test_{ts}{name}.png"
        artifacts_dir = Path("tests", "artifacts")
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        file_path = artifacts_dir / file_name
        driver.save_screenshot(str(file_path))
        return str(file_path)
