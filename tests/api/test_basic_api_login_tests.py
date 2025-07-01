from http import HTTPStatus

import pytest

from helper_functions_for_tests.login_tests_helpers import call_verify_login
from utils.markers import api


@api
@pytest.mark.parametrize(
    "email, password, expected_code",
    [
        ("fixture_user", "fixture_pass", HTTPStatus.OK),
        pytest.param(
            "invalid@email.com",
            "wrongpass",
            HTTPStatus.UNAUTHORIZED,
            marks=pytest.mark.xfail(
                reason="BUG: API returns 404 for invalid login instead of 401. See BUGS.md #1"
            ),
        ),
        (None, "any", HTTPStatus.BAD_REQUEST),
        ("fixture_user", None, HTTPStatus.BAD_REQUEST),
    ],
)
def test_verify_login_cases(email, password, expected_code, user_api):
    resp = call_verify_login(email, password, user_api)
    assert resp.json().get("responseCode") == expected_code
