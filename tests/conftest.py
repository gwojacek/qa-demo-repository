import builtins
import logging
import os
import time
from pathlib import Path

import pytest
from dotenv import find_dotenv, load_dotenv
from faker import Faker
from pytest_html import extras  # important for extras.html()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from utils.api_requests import create_account
from utils.payloads import user_create_payload

fake = Faker("pl_PL")  # Use Polish locale for more realistic data
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    force=True,
)


def load_selected_env():
    # ENV_TYPE can be 'local' or 'staging'; default to 'local'
    env_type = os.environ.get("ENV_TYPE", "local")
    env_file = f"localconf_{env_type}.env"
    # Fallback to local if staging not present
    if not os.path.exists(env_file) and env_type != "local":
        env_file = "localconf_local.env"
    load_dotenv(find_dotenv(env_file), override=True)
    # Nicely formatted info for pytest header
    return f"\n=======\n[env] Loading environment: {env_file}\n=======\n"


# Load env and get the message
_env_msg = load_selected_env()


def pytest_report_header(config):
    return _env_msg


# ---- printing helper -------------------------------------------------------
_ORIG_PRINT = builtins.print


def _print_and_log(*args, **kwargs):
    """Forward print calls to the logger so they appear with xdist."""
    msg = " ".join(str(a) for a in args)
    logging.getLogger("PRINT").info(msg)
    _ORIG_PRINT(*args, **kwargs)


def pytest_configure(config):
    builtins.print = _print_and_log


def pytest_unconfigure(config):
    builtins.print = _ORIG_PRINT


def _make_screenshot_path(item):
    ts = time.strftime("%Y%m%d-%H%M%S")
    safe = item.nodeid.replace("::", "_").replace("/", "_")
    path = Path(item.config.rootpath, "tests", "artifacts", f"{ts}_{safe}.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when != "call":
        return

    # Consider all non-passed outcomes: failed, xfailed (skipped), xpassed
    if report.outcome not in ("failed", "skipped"):
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    # Save screenshot
    p = _make_screenshot_path(item)
    driver.save_screenshot(str(p))

    # Relative path to HTML file
    html_report_path = item.config.option.htmlpath
    rel_path = os.path.relpath(p, start=os.path.dirname(html_report_path))

    # Embed clickable screenshot
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


@pytest.fixture
def new_user_api():
    user = user_create_payload()
    req = create_account(user)
    return {"user": user, "request": req}
