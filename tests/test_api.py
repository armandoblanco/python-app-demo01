"""
Tests for the backend API
"""
import pytest
from backend.api import app, products

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_get_all_products(client):
    """Test getting all products"""
    response = client.get('/api/products')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert len(data['data']) == 10
    assert data['count'] == 10

def test_get_products_by_category_watch(client):
    """Test filtering products by watch category"""
    response = client.get('/api/products?category=watch')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 5
    for product in data['data']:
        assert product['category'] == 'watch'

def test_get_products_by_category_jewelry(client):
    """Test filtering products by jewelry category"""
    response = client.get('/api/products?category=jewelry')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 5
    for product in data['data']:
        assert product['category'] == 'jewelry'

def test_search_products(client):
    """Test searching products"""
    response = client.get('/api/products?search=rolex')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) >= 1
    assert 'rolex' in data['data'][0]['name'].lower()

def test_search_products_no_results(client):
    """Test searching products with no results"""
    response = client.get('/api/products?search=nonexistent')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 0

def test_search_and_filter_combined(client):
    """Test combining search and category filter"""
    response = client.get('/api/products?category=watch&search=omega')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) >= 1
    for product in data['data']:
        assert product['category'] == 'watch'
        assert 'omega' in product['name'].lower()

def test_get_product_by_id(client):
    """Test getting a specific product by ID"""
    response = client.get('/api/products/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['id'] == 1
    assert data['data']['name'] == 'Rolex Submariner'

def test_get_product_not_found(client):
    """Test getting a non-existent product"""
    response = client.get('/api/products/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data

def test_get_categories(client):
    """Test getting categories"""
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 3
    category_ids = [cat['id'] for cat in data['data']]
    assert 'all' in category_ids
    assert 'watch' in category_ids
    assert 'jewelry' in category_ids

def test_404_endpoint(client):
    """Test 404 error handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False

def test_products_have_required_fields(client):
    """Test that all products have required fields"""
    response = client.get('/api/products')
    data = response.get_json()
    
    required_fields = ['id', 'name', 'category', 'price', 'description', 'image']
    
    for product in data['data']:
        for field in required_fields:
            assert field in product
            assert product[field] is not None

def test_product_prices_are_valid(client):
    """Test that all product prices are valid numbers"""
    response = client.get('/api/products')
    data = response.get_json()
    
    for product in data['data']:
        assert isinstance(product['price'], (int, float))
        assert product['price'] > 0
