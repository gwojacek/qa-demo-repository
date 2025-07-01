from utils.api_requests import verify_login_no_email, verify_login_valid
from utils.request_builder import Request, RequestMethod


def call_verify_login(email, password, user_api):
    """Centralized logic for API login calls with fixture user support."""
    if email == "fixture_user":
        email = user_api.email
    if password == "fixture_pass":
        password = user_api.password

    # Smart dispatch for API
    if email is not None and password is not None:
        return verify_login_valid(email, password)
    if email is None and password is not None:
        return verify_login_no_email(password)
    if email is not None and password is None:
        return (
            Request(RequestMethod.POST)
            .path("/api/verifyLogin")
            .data({"email": email})
            .send()
        )
    return Request(RequestMethod.POST).path("/api/verifyLogin").send()
