import pytest

from utils.momo_crawler import crawler


@pytest.mark.vcr
def test_ok():
    items, error_items = crawler('iphone', [])
    assert len(items) > 0
    assert len(error_items) == 0
    assert isinstance(items, list)
    assert isinstance(error_items, list)
