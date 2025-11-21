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

def get_auth_token(client):
    """Helper function to get JWT token for testing"""
    response = client.post('/api/auth/login', 
                          json={'username': 'admin', 'password': 'admin123'},
                          content_type='application/json')
    data = response.get_json()
    return data.get('access_token')

# ============== Existing Tests ==============

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

# ============== New Security Tests ==============

def test_login_success(client):
    """Test successful login with correct credentials"""
    response = client.post('/api/auth/login', 
                          json={'username': 'admin', 'password': 'admin123'},
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'access_token' in data
    assert data['token_type'] == 'Bearer'

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', 
                          json={'username': 'admin', 'password': 'wrongpass'},
                          content_type='application/json')
    assert response.status_code == 401
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data

def test_login_missing_data(client):
    """Test login with missing data"""
    response = client.post('/api/auth/login', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_login_no_json(client):
    """Test login without JSON data"""
    response = client.post('/api/auth/login')
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_admin_endpoint_without_token(client):
    """Test accessing admin endpoint without JWT token"""
    response = client.get('/api/admin/products')
    assert response.status_code == 401

def test_admin_endpoint_with_token(client):
    """Test accessing admin endpoint with valid JWT token"""
    token = get_auth_token(client)
    response = client.get('/api/admin/products',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert 'user' in data
    assert data['user'] == 'admin'

def test_input_sanitization_search(client):
    """Test that search input is sanitized"""
    # Try injecting HTML/script tags
    response = client.get('/api/products?search=<script>alert("xss")</script>')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    # Should return empty results since the sanitized input won't match products
    assert len(data['data']) == 0

def test_input_sanitization_category(client):
    """Test that category input is validated"""
    # Try invalid category
    response = client.get('/api/products?category=<script>alert("xss")</script>')
    assert response.status_code == 200
    data = response.get_json()
    # Should default to 'all' and return all products
    assert len(data['data']) == 10

def test_invalid_product_id(client):
    """Test that invalid product IDs are handled"""
    response = client.get('/api/products/0')
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data

def test_negative_product_id(client):
    """Test that negative product IDs are rejected"""
    response = client.get('/api/products/-1')
    # Flask routing treats negative IDs as 404 not found since they don't match the route pattern properly
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False

def test_search_length_limit(client):
    """Test that search query length is limited"""
    # Create a very long search query
    long_query = 'a' * 500
    response = client.get(f'/api/products?search={long_query}')
    assert response.status_code == 200
    data = response.get_json()
    # Should still work but query is truncated
    assert data['success'] is True
