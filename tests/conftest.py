import os
import time
from pathlib import Path

import pytest
from pytest_html import extras  # important for extras.html()
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

        # Save screenshot
        p = _make_screenshot_path(item)
        driver.save_screenshot(str(p))

        # Relative path to HTML file
        html_report_path = item.config.option.htmlpath
        rel_path = os.path.relpath(p, start=os.path.dirname(html_report_path))

        # Embed manually clickable <img> tag

        html_snippet = (
            f'<div><img src="{rel_path}" alt="screenshot" '
            f'style="width:600px; height:auto; display:block; float:right; margin:10px;" '
            f'onclick="window.open(this.src)"/></div>'
        )

        extra = getattr(report, "extra", [])
        extra.append(extras.html(html_snippet))
        report.extras = extra


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
