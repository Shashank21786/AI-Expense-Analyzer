from app.services.category_service import get_merchant_category


def test_swiggy_is_food():
    assert get_merchant_category("SWIGGY") == "Food"


def test_zomato_is_food():
    assert get_merchant_category("Zomato") == "Food"


def test_amazon_is_shopping():
    assert get_merchant_category("Amazon") == "Shopping"


def test_uber_is_transport():
    assert get_merchant_category("Uber") == "Transport"


def test_netflix_is_entertainment():
    assert get_merchant_category("Netflix") == "Entertainment"


def test_unknown_merchant_returns_none():
    assert get_merchant_category("Unknown Store") is None


def test_none_merchant_returns_none():
    assert get_merchant_category(None) is None