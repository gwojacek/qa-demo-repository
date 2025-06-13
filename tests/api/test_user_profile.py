# In your test file:
import logging
from http import HTTPStatus

from utils.api_requests import create_account
from utils.markers import usertests
from utils.payloads import user_create_payload

logger = logging.getLogger(__name__)


@usertests
def test_create_account():
    user = user_create_payload()
    req = create_account(user).send()
    logger.info("THIS IS A TEST")
    logger.info("THIS IS A TEST")
    assert (
        req.status_code == HTTPStatus.OK
    ), f"Request failed with status {req.status_code}: {req.content}"
    logger.info(f"requests: {req.text}")
