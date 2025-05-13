import os
import time
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def _make_screenshot_path(item):
    ts = time.strftime("%Y%m%d-%H%M%S")
    safe = item.nodeid.replace("::", "_").replace("/", "_")
    path = Path(__file__).parent / "artifacts" / f"{ts}_{safe}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if not driver:
            return
        p = _make_screenshot_path(item)
        driver.save_screenshot(str(p))
        html = item.config.pluginmanager.getplugin("html")
        if html:
            rel = os.path.relpath(p, start=Path(item.config.option.htmlpath).parent)
            extras = getattr(report, "extras", [])
            extras.append(html.extras.image(rel))
            report.extras = extras


@pytest.fixture(scope="session")
def driver():
    browser = os.getenv("BROWSER", "chrome").lower()
    remote = os.getenv("SELENIUM_REMOTE_URL")
    headless = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")

    if browser == "firefox":
        opts = FirefoxOptions()
        # start maximized so it's visible within the VNC desktop
        opts.add_argument("--start-maximized")
        if headless:
            opts.add_argument("--headless")
        opts.add_argument("--width=2560")
        opts.add_argument("--height=1440")
    else:
        opts = ChromeOptions()
        # start maximized so it's visible within the VNC desktop
        opts.add_argument("--start-maximized")
        if headless:
            opts.add_argument("--headless=new")
            opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--window-size=2560,1440")

    drv = webdriver.Remote(command_executor=remote, options=opts)
    # ensure the viewport matches the container's screen
    drv.set_window_size(2560, 1440)
    yield drv
    drv.quit()
