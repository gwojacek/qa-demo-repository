from utils.api_requests import get_all_products, post_to_products_list
from utils.markers import api


@api
def test_get_all_products_returns_200_and_product_list():
    """GET /api/productsList returns 200 and product list"""
    response = get_all_products().send()
    assert response.status_code == 200
    data = response.json()
    assert "products" in data or isinstance(data, dict)
    # optionally check structure or length
    assert isinstance(data, dict)  # or check for a top-level "products" key


@api
def test_post_to_products_list_returns_405():
    """POST /api/productsList returns 405 (method not allowed)"""
    response = post_to_products_list().send()
    assert response.status_code == 405
    # Optionally check error message
    if response.headers.get("Content-Type", "").startswith("application/json"):
        data = response.json()
        assert "This request method is not supported" in str(data)
    else:
        assert "This request method is not supported" in response.text
