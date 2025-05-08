import os
import time
import base64
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _make_screenshot_path(item):
    ts = time.strftime("%Y%m%d-%H%M%S")
    safe = item.nodeid.replace("::", "_").replace("/", "_")
    fname = f"{ts}_{safe}.png"

    artifacts_dir = Path(__file__).parent / "artifacts"  # <== saves to tests/artifacts
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    return artifacts_dir / fname


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if not driver:
            return

        screenshot_path = _make_screenshot_path(item)
        driver.save_screenshot(str(screenshot_path))

        html_plugin = item.config.pluginmanager.getplugin("html")
        if html_plugin:
            report_dir = Path(item.config.option.htmlpath).parent
            rel_path = os.path.relpath(screenshot_path, start=report_dir)
            extras = getattr(report, "extras", [])
            extras.append(html_plugin.extras.image(rel_path))
            report.extras = extras


@pytest.fixture(scope="session")
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    remote = os.getenv("SELENIUM_REMOTE_URL", "http://selenium:4444/wd/hub")
    drv = webdriver.Remote(command_executor=remote, options=opts)
    yield drv
    drv.quit()
