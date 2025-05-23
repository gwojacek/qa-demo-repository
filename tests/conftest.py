import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

def _make_screenshot_path(item):
    ts = time.strftime("%Y%m%d-%H%M%S")
    safe = item.nodeid.replace("::", "_").replace("/", "_")
    path = Path(item.config.rootpath, "tests", "artifacts", f"{ts}_{safe}.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if not driver:
            return

        # Save screenshot to file
        p = _make_screenshot_path(item)
        driver.save_screenshot(str(p))

        # Compute relative path for HTML report
        rel_path = os.path.relpath(p, start=os.path.dirname(item.config.option.htmlpath))

        # Attach as image EXTRA — this is what gives you a clickable thumbnail on the right
        html = item.config.pluginmanager.getplugin("html")
        extras = getattr(report, "extras", [])
        extras.append(html.extras.image(rel_path))
        report.extras = extras


@pytest.fixture(scope="session")
def driver():
    browser = os.getenv("BROWSER", "chrome").lower()
    remote = os.getenv("SELENIUM_REMOTE_URL")
    headless = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")

    # Use ChromeOptions for both Chrome and Opera
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-dev-shm-usage")
        # Opera-specific tweak for GPU
        if browser == "opera":
            opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=2560,1440")

    driver = webdriver.Remote(command_executor=remote, options=opts)
    driver.set_window_size(2560, 1440)
    yield driver
    driver.quit()
