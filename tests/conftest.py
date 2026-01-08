import logging
import os
from http import HTTPStatus

import pytest
from faker import Faker
from pytest_html import extras

from components.consent_popup import ConsentPopup
from tests.conftest_helpers import (
    configure_print_logging,
    load_selected_env,
    make_screenshot_path,
    restore_print_logging,
)
from utils.api_requests import create_account, delete_account, verify_login_valid
from utils.payloads import User, user_create_payload

fake = Faker("pl_PL")
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    force=True,
)

# Load env and get the message
_env_msg = load_selected_env()


def pytest_report_header(config):
    return _env_msg


def pytest_configure(config):
    configure_print_logging()


def pytest_unconfigure(config):
    restore_print_logging()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when != "call":
        return

    # Consider all non-passed outcomes: failed, xfailed (skipped), xpassed
    if report.outcome not in ("failed", "skipped"):
        return

    page = item.funcargs.get("page")
    if not page:
        return

    # Save screenshot
    p = make_screenshot_path(item)
    page.screenshot(path=p)

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


@pytest.fixture(scope="function")
def page_on_address(page):
    address = os.environ.get("ADDRESS")
    if not address:
        raise RuntimeError("ADDRESS env var not set!")
    page.goto(address)
    ConsentPopup(page).accept()  # Handles the popup if present

    yield page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 2560,
            "height": 1440,
        },
    }


@pytest.fixture(scope="session")
def user_api(request):
    user_data = user_create_payload()
    other = {
        k: v for k, v in user_data.items() if k not in ("name", "email", "password")
    }
    user = User(user_data["name"], user_data["email"], user_data["password"], other)
    create_account(user_data)
    yield user
    # Default: delete unless param==False
    delete = getattr(request, "param", True)
    if delete:
        delete_account(user.email, user.password)
        resp = verify_login_valid(user.email, user.password)
        assert resp.json().get("responseCode") == HTTPStatus.NOT_FOUND
