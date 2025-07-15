from http import HTTPStatus

import pytest

from pages.delete_account_page import DeleteAccountPage
from pages.login_page import LoginPage
from utils.api_requests import verify_login_valid
from utils.markers import usertests


@usertests
@pytest.mark.parametrize("user_api", [False], indirect=True)  # fixture parametrization
def test_delete_account_via_ui_and_verify_api(driver, user_api):
    """Delete an account through the UI and verify via API that it was removed."""

    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(user_api.email, user_api.password)
    DeleteAccountPage(driver).delete_account_and_continue()
    resp = verify_login_valid(user_api.email, user_api.password)
    assert resp.json().get("responseCode") == HTTPStatus.NOT_FOUND
    # BUG: API returns 200 instead of 404 (see https://github.com/gwojacek/qa-demo-repository/issues/12)
