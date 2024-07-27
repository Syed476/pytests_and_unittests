# test_data_processor.py
import pytest
from src.data_processor import process_sales_data, DataProcessingError


@pytest.fixture
def sample_sales_data():
    return [
        {'product': 'A', 'quantity': 2, 'price': 10},
        {'product': 'B', 'quantity': 3, 'price': 15},
        {'product': 'A', 'quantity': 1, 'price': 10},
    ]


def test_process_sales_data(sample_sales_data):
    result = process_sales_data(sample_sales_data)

    assert len(result) == 2
    assert list(result.columns) == ['product', 'total', 'quantity', 'average_price']

    product_a = result[result['product'] == 'A'].iloc[0]
    assert product_a['total'] == 30
    assert product_a['quantity'] == 3
    assert product_a['average_price'] == 10

    product_b = result[result['product'] == 'B'].iloc[0]
    assert product_b['total'] == 45
    assert product_b['quantity'] == 3
    assert product_b['average_price'] == 15


@pytest.mark.parametrize("data,expected_products", [
    ([{'product': 'A', 'quantity': 1, 'price': 10}], ['A']),
    ([{'product': 'A', 'quantity': 1, 'price': 10},
      {'product': 'B', 'quantity': 2, 'price': 20}], ['A', 'B']),
])
def test_process_sales_data_products(data, expected_products):
    result = process_sales_data(data)
    assert list(result['product']) == expected_products


def test_empty_input():
    with pytest.raises(DataProcessingError, match="Input data is empty"):
        process_sales_data([])


def test_missing_column():
    invalid_data = [{'product': 'A', 'quantity': 1}]  # Missing 'price'
    with pytest.raises(DataProcessingError, match="Input data must contain columns"):
        process_sales_data(invalid_data)


def test_non_numeric_data():
    invalid_data = [{'product': 'A', 'quantity': 'invalid', 'price': 10}]
    with pytest.raises(DataProcessingError, match="Quantity and price must be numeric"):
        process_sales_data(invalid_data)


def test_negative_values():
    invalid_data = [{'product': 'A', 'quantity': -1, 'price': 10}]
    with pytest.raises(DataProcessingError, match="Quantity and price cannot be negative"):
        process_sales_data(invalid_data)


def test_division_by_zero():
    data = [{'product': 'A', 'quantity': 0, 'price': 10}]
    result = process_sales_data(data)
    assert result.loc[0, 'average_price'] == 0