from utils.request_builder import Request, RequestMethod

# API wrapper for "automationexercise.com"


def get_all_products():
    return Request(RequestMethod.GET).path("/api/productsList")


def post_to_products_list():
    return Request(RequestMethod.POST).path("/api/productsList")


def get_all_brands():
    return Request(RequestMethod.GET).path("/api/brandsList")


def put_to_brands_list():
    return Request(RequestMethod.PUT).path("/api/brandsList")


def search_product(search_term: str):
    """
    Params:
        search_term (str)
    """
    return (
        Request(RequestMethod.POST)
        .path("/api/searchProduct")
        .data({"search_product": search_term})
    )


def search_product_no_param():
    return Request(RequestMethod.POST).path("/api/searchProduct")


def verify_login_valid(email: str, password: str):
    """
    Params:
        email (str)
        password (str)
    """
    return (
        Request(RequestMethod.POST)
        .path("/api/verifyLogin")
        .data({"email": email, "password": password})
    )


def verify_login_no_email(password: str):
    """
    Params:
        password (str)
    """
    return (
        Request(RequestMethod.POST)
        .path("/api/verifyLogin")
        .data({"password": password})
    )


def verify_login_delete():
    return Request(RequestMethod.DELETE).path("/api/verifyLogin")


def verify_login_invalid(email: str, password: str):
    """
    Params:
        email (str)
        password (str)
    """
    return (
        Request(RequestMethod.POST)
        .path("/api/verifyLogin")
        .data({"email": email, "password": password})
    )


def create_account(user: dict):
    """
    Params in user dict (all required):
        name, email, password, title, birth_date, birth_month, birth_year,
        firstname, lastname, company, address1, address2, country, zipcode,
        state, city, mobile_number
    """
    return Request(RequestMethod.POST).path("/api/createAccount").data(user)


def delete_account(email: str, password: str):
    """
    Params:
        email (str)
        password (str)
    """
    return (
        Request(RequestMethod.DELETE)
        .path("/api/deleteAccount")
        .data({"email": email, "password": password})
    )


def update_account(user: dict):
    """
    Params in user dict (all same as create_account):
        name, email, password, title, birth_date, birth_month, birth_year,
        firstname, lastname, company, address1, address2, country, zipcode,
        state, city, mobile_number
    """
    return Request(RequestMethod.PUT).path("/api/updateAccount").data(user)


def get_user_detail_by_email(email: str):
    """
    Params:
        email (str)
    """
    return (
        Request(RequestMethod.GET)
        .path("/api/getUserDetailByEmail")
        .params({"email": email})
    )
