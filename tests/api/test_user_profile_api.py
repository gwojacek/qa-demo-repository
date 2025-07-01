import logging
from http import HTTPStatus

from utils.api_requests import (create_account, delete_account,
                                verify_login_valid)
from utils.markers import api, usertests
from utils.payloads import user_create_payload

logger = logging.getLogger(__name__)


@api
@usertests
def test_create_delete_account():
    user = user_create_payload()
    req = create_account(user)
    assert req.json().get("responseCode") == HTTPStatus.CREATED
    # BUG: API returns 200 for deleted users instead of 201 (see BUGS.md no. 1)

    delete_account(user["email"], user["password"])
    resp = verify_login_valid(user["email"], user["password"])
    # BUG: API returns 200 for deleted users instead of 404 (see BUGS.md no. 1)
    assert resp.json().get("responseCode") == HTTPStatus.NOT_FOUND


@api
@usertests
def test_create_account_with_fixture(user_api):
    pass
