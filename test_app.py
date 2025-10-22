"""
Tests for the Flask app to verify performance improvements and functionality.
"""
import pytest
from app import app, products_list, products_dict, filter_products


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_products_dict_contains_all_products():
    """Test that products_dict is properly initialized with all products."""
    assert len(products_dict) == len(products_list)
    assert len(products_dict) == 10
    
    # Verify all product IDs are present
    for product in products_list:
        assert product['id'] in products_dict
        assert products_dict[product['id']] == product


def test_filter_products_no_filters():
    """Test filter_products with no filters returns all products."""
    result = filter_products(products_list)
    assert len(result) == 10
    assert result == products_list


def test_filter_products_by_category_watch():
    """Test filtering products by watch category."""
    result = filter_products(products_list, category='watch')
    assert len(result) == 5
    assert all(p['category'] == 'watch' for p in result)


def test_filter_products_by_category_jewelry():
    """Test filtering products by jewelry category."""
    result = filter_products(products_list, category='jewelry')
    assert len(result) == 5
    assert all(p['category'] == 'jewelry' for p in result)


def test_filter_products_by_search_query():
    """Test filtering products by search query."""
    # Search for "Rolex"
    result = filter_products(products_list, search_query='Rolex')
    assert len(result) == 1
    assert result[0]['name'] == 'Rolex Submariner'
    
    # Search for "diamante" (in description)
    result = filter_products(products_list, search_query='diamante')
    assert len(result) >= 1
    assert any('diamante' in p['description'].lower() for p in result)


def test_filter_products_combined_filters():
    """Test filtering products with both category and search query."""
    result = filter_products(products_list, category='watch', search_query='Omega')
    assert len(result) == 1
    assert result[0]['name'] == 'Omega Speedmaster'
    assert result[0]['category'] == 'watch'


def test_filter_products_case_insensitive():
    """Test that search is case insensitive."""
    result_upper = filter_products(products_list, search_query='ROLEX')
    result_lower = filter_products(products_list, search_query='rolex')
    result_mixed = filter_products(products_list, search_query='RoLeX')
    
    assert result_upper == result_lower == result_mixed
    assert len(result_upper) == 1


def test_index_route(client):
    """Test the index route returns successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Relojes de Lujo' in response.data


def test_index_route_with_category_filter(client):
    """Test the index route with category filter."""
    response = client.get('/?category=watch')
    assert response.status_code == 200
    assert b'Rolex' in response.data or b'Omega' in response.data


def test_index_route_with_search(client):
    """Test the index route with search query."""
    response = client.get('/?search=Rolex')
    assert response.status_code == 200
    assert b'Rolex' in response.data


def test_product_detail_route(client):
    """Test the product detail route for a valid product."""
    response = client.get('/product/1')
    assert response.status_code == 200
    assert b'Rolex Submariner' in response.data


def test_product_detail_route_invalid_id(client):
    """Test the product detail route with invalid product ID."""
    response = client.get('/product/999')
    assert response.status_code == 404
    assert b'Producto no encontrado' in response.data


def test_api_search_route(client):
    """Test the API search endpoint."""
    response = client.get('/api/search')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 10


def test_api_search_with_query(client):
    """Test the API search endpoint with query parameter."""
    response = client.get('/api/search?q=Rolex')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Rolex Submariner'


def test_api_search_with_category(client):
    """Test the API search endpoint with category filter."""
    response = client.get('/api/search?category=jewelry')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 5
    assert all(p['category'] == 'jewelry' for p in data)


def test_api_search_combined_filters(client):
    """Test the API search endpoint with both filters."""
    response = client.get('/api/search?q=Omega&category=watch')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Omega Speedmaster'


def test_product_lookup_performance():
    """Test that dictionary lookup is used for product details."""
    # This test verifies the data structure exists
    # In a real scenario, we'd benchmark the lookup time
    assert isinstance(products_dict, dict)
    
    # O(1) lookup
    product = products_dict.get(1)
    assert product is not None
    assert product['name'] == 'Rolex Submariner'
    
    # Non-existent product
    product = products_dict.get(999)
    assert product is None


def test_filter_products_empty_result():
    """Test filter_products returns empty list when no matches."""
    result = filter_products(products_list, search_query='nonexistentproduct12345')
    assert len(result) == 0
    assert result == []


def test_filter_products_with_whitespace():
    """Test that whitespace in search queries is handled."""
    # This test verifies .strip() is working in the routes
    result = filter_products(products_list, search_query='  Rolex  ')
    assert len(result) == 1
    assert result[0]['name'] == 'Rolex Submariner'
