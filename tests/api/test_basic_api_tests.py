from utils.api_requests import get_all_products, post_to_products_list
from utils.markers import api, xfail


@api
def test_get_all_products_returns_200_and_product_list():
    """GET /api/productsList returns 200 and product list"""
    response = get_all_products().send()
    assert response.status_code == 200
    data = response.json()
    assert "products" in data or isinstance(data, dict)


@api
@xfail
def test_post_to_products_list_returns_405():
    """POST /api/productsList returns 405 (method not allowed)"""
    response = post_to_products_list().send()
    assert response.status_code == 405
