import pytest
from app import app, products


@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIndexRoute:
    """Test cases for the main index route"""
    
    def test_index_loads_successfully(self, client):
        """Test that the main page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Relojes de Lujo' in response.data
    
    def test_index_displays_all_products(self, client):
        """Test that all products are displayed by default"""
        response = client.get('/')
        assert response.status_code == 200
        # Check that some product names appear
        assert b'Rolex Submariner' in response.data
        assert b'Collar de Diamantes' in response.data
    
    def test_index_filter_by_watch_category(self, client):
        """Test filtering products by watch category"""
        response = client.get('/?category=watch')
        assert response.status_code == 200
        # Should contain watch products
        assert b'Rolex Submariner' in response.data
        # Should not contain jewelry if properly filtered on page
        assert b'active' in response.data  # Active filter button
    
    def test_index_filter_by_jewelry_category(self, client):
        """Test filtering products by jewelry category"""
        response = client.get('/?category=jewelry')
        assert response.status_code == 200
        # Should contain jewelry products
        assert b'Collar de Diamantes' in response.data
        assert b'active' in response.data  # Active filter button
    
    def test_index_search_functionality(self, client):
        """Test search functionality"""
        response = client.get('/?search=rolex')
        assert response.status_code == 200
        assert b'Rolex Submariner' in response.data
    
    def test_index_search_case_insensitive(self, client):
        """Test that search is case insensitive"""
        response = client.get('/?search=ROLEX')
        assert response.status_code == 200
        assert b'Rolex Submariner' in response.data
    
    def test_index_search_in_description(self, client):
        """Test that search works in product descriptions"""
        response = client.get('/?search=buceo')
        assert response.status_code == 200
        assert b'Rolex Submariner' in response.data
    
    def test_index_search_no_results(self, client):
        """Test search with no matching results"""
        response = client.get('/?search=nonexistentproduct12345')
        assert response.status_code == 200
        assert b'No se encontraron productos' in response.data
    
    def test_index_combined_filter_and_search(self, client):
        """Test combining category filter with search"""
        response = client.get('/?category=watch&search=omega')
        assert response.status_code == 200
        assert b'Omega Speedmaster' in response.data


class TestProductDetailRoute:
    """Test cases for product detail route"""
    
    def test_product_detail_valid_id(self, client):
        """Test accessing a valid product detail page"""
        response = client.get('/product/1')
        assert response.status_code == 200
        assert b'Rolex Submariner' in response.data
    
    def test_product_detail_another_valid_id(self, client):
        """Test accessing another valid product"""
        response = client.get('/product/6')
        assert response.status_code == 200
        assert b'Collar de Diamantes' in response.data
    
    def test_product_detail_invalid_id(self, client):
        """Test accessing a non-existent product"""
        response = client.get('/product/999')
        assert response.status_code == 404
        assert b'Producto no encontrado' in response.data
    
    def test_product_detail_displays_price(self, client):
        """Test that product price is displayed with comma formatting"""
        response = client.get('/product/1')
        assert response.status_code == 200
        assert b'12,500' in response.data


class TestAPISearch:
    """Test cases for the API search endpoint"""
    
    def test_api_search_returns_json(self, client):
        """Test that API search returns JSON"""
        response = client.get('/api/search')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_api_search_all_products(self, client):
        """Test API returns all products without filters"""
        response = client.get('/api/search')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 10  # Should return all 10 products
    
    def test_api_search_with_query(self, client):
        """Test API search with a query parameter"""
        response = client.get('/api/search?q=rolex')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
        assert any(p['name'] == 'Rolex Submariner' for p in data)
    
    def test_api_search_by_category(self, client):
        """Test API search filtered by category"""
        response = client.get('/api/search?category=watch')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 5  # Should return 5 watches
        assert all(p['category'] == 'watch' for p in data)
    
    def test_api_search_jewelry_category(self, client):
        """Test API search for jewelry category"""
        response = client.get('/api/search?category=jewelry')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 5  # Should return 5 jewelry items
        assert all(p['category'] == 'jewelry' for p in data)
    
    def test_api_search_combined_query_and_category(self, client):
        """Test API search with both query and category"""
        response = client.get('/api/search?q=oro&category=jewelry')
        assert response.status_code == 200
        data = response.get_json()
        assert all(p['category'] == 'jewelry' for p in data)
        # Should find products with "oro" in name or description
        assert len(data) >= 1
    
    def test_api_search_case_insensitive(self, client):
        """Test that API search is case insensitive"""
        response = client.get('/api/search?q=OMEGA')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
        assert any(p['name'] == 'Omega Speedmaster' for p in data)
    
    def test_api_search_no_results(self, client):
        """Test API search with no results"""
        response = client.get('/api/search?q=nonexistent12345')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 0


class TestProductsData:
    """Test cases for the products data structure"""
    
    def test_products_count(self):
        """Test that there are exactly 10 products"""
        assert len(products) == 10
    
    def test_products_have_required_fields(self):
        """Test that all products have required fields"""
        required_fields = ['id', 'name', 'category', 'price', 'description', 'image']
        for product in products:
            for field in required_fields:
                assert field in product, f"Product {product.get('id')} missing field {field}"
    
    def test_product_ids_are_unique(self):
        """Test that all product IDs are unique"""
        ids = [p['id'] for p in products]
        assert len(ids) == len(set(ids)), "Product IDs are not unique"
    
    def test_product_categories_are_valid(self):
        """Test that product categories are either 'watch' or 'jewelry'"""
        valid_categories = {'watch', 'jewelry'}
        for product in products:
            assert product['category'] in valid_categories
    
    def test_product_prices_are_positive(self):
        """Test that all product prices are positive numbers"""
        for product in products:
            assert isinstance(product['price'], (int, float))
            assert product['price'] > 0
    
    def test_watches_count(self):
        """Test that there are 5 watches"""
        watches = [p for p in products if p['category'] == 'watch']
        assert len(watches) == 5
    
    def test_jewelry_count(self):
        """Test that there are 5 jewelry items"""
        jewelry = [p for p in products if p['category'] == 'jewelry']
        assert len(jewelry) == 5
    
    def test_product_names_are_not_empty(self):
        """Test that all products have non-empty names"""
        for product in products:
            assert product['name'] and len(product['name']) > 0
    
    def test_product_descriptions_are_not_empty(self):
        """Test that all products have non-empty descriptions"""
        for product in products:
            assert product['description'] and len(product['description']) > 0


class TestAppConfiguration:
    """Test cases for Flask app configuration"""
    
    def test_app_exists(self):
        """Test that the Flask app is created"""
        assert app is not None
    
    def test_app_is_flask_instance(self):
        """Test that app is a Flask instance"""
        from flask import Flask
        assert isinstance(app, Flask)
    
    def test_testing_mode(self, client):
        """Test that testing mode can be enabled"""
        assert app.config['TESTING'] == True


# Run tests if executed directly
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
