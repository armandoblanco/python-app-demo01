<?php
/**
 * Tests for the PHP backend API
 * Mirrors the pytest tests from tests/test_api.py
 */

use PHPUnit\Framework\TestCase;

class ApiTest extends TestCase
{
    private $baseUrl = 'http://localhost:8080';
    
    /**
     * Make HTTP GET request
     */
    private function get($endpoint)
    {
        $url = $this->baseUrl . $endpoint;
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HEADER, false);
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        return [
            'status_code' => $httpCode,
            'data' => json_decode($response, true)
        ];
    }
    
    public function testHealthCheck()
    {
        $response = $this->get('/api/health.php');
        $this->assertEquals(200, $response['status_code']);
        $this->assertEquals('healthy', $response['data']['status']);
        $this->assertArrayHasKey('version', $response['data']);
    }
    
    public function testGetAllProducts()
    {
        $response = $this->get('/api/products.php');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertArrayHasKey('data', $response['data']);
        $this->assertEquals(10, count($response['data']['data']));
        $this->assertEquals(10, $response['data']['count']);
    }
    
    public function testGetProductsByCategoryWatch()
    {
        $response = $this->get('/api/products.php?category=watch');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertEquals(5, count($response['data']['data']));
        
        foreach ($response['data']['data'] as $product) {
            $this->assertEquals('watch', $product['category']);
        }
    }
    
    public function testGetProductsByCategoryJewelry()
    {
        $response = $this->get('/api/products.php?category=jewelry');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertEquals(5, count($response['data']['data']));
        
        foreach ($response['data']['data'] as $product) {
            $this->assertEquals('jewelry', $product['category']);
        }
    }
    
    public function testSearchProducts()
    {
        $response = $this->get('/api/products.php?search=rolex');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertGreaterThanOrEqual(1, count($response['data']['data']));
        $this->assertStringContainsStringIgnoringCase('rolex', $response['data']['data'][0]['name']);
    }
    
    public function testSearchProductsNoResults()
    {
        $response = $this->get('/api/products.php?search=nonexistent');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertEquals(0, count($response['data']['data']));
    }
    
    public function testSearchAndFilterCombined()
    {
        $response = $this->get('/api/products.php?category=watch&search=omega');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertGreaterThanOrEqual(1, count($response['data']['data']));
        
        foreach ($response['data']['data'] as $product) {
            $this->assertEquals('watch', $product['category']);
            $this->assertStringContainsStringIgnoringCase('omega', $product['name']);
        }
    }
    
    public function testGetProductById()
    {
        $response = $this->get('/api/product.php?id=1');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertEquals(1, $response['data']['data']['id']);
        $this->assertEquals('Rolex Submariner', $response['data']['data']['name']);
    }
    
    public function testGetProductNotFound()
    {
        $response = $this->get('/api/product.php?id=999');
        $this->assertEquals(404, $response['status_code']);
        $this->assertFalse($response['data']['success']);
        $this->assertArrayHasKey('error', $response['data']);
    }
    
    public function testGetCategories()
    {
        $response = $this->get('/api/categories.php');
        $this->assertEquals(200, $response['status_code']);
        $this->assertTrue($response['data']['success']);
        $this->assertEquals(3, count($response['data']['data']));
        
        $categoryIds = array_column($response['data']['data'], 'id');
        $this->assertContains('all', $categoryIds);
        $this->assertContains('watch', $categoryIds);
        $this->assertContains('jewelry', $categoryIds);
    }
    
    public function testProductsHaveRequiredFields()
    {
        $response = $this->get('/api/products.php');
        
        $requiredFields = ['id', 'name', 'category', 'price', 'description', 'image'];
        
        foreach ($response['data']['data'] as $product) {
            foreach ($requiredFields as $field) {
                $this->assertArrayHasKey($field, $product);
                $this->assertNotNull($product[$field]);
            }
        }
    }
    
    public function testProductPricesAreValid()
    {
        $response = $this->get('/api/products.php');
        
        foreach ($response['data']['data'] as $product) {
            $this->assertIsNumeric($product['price']);
            $this->assertGreaterThan(0, $product['price']);
        }
    }
}
