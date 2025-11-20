<?php
/**
 * Products endpoints
 * GET /api/products - Get all products with optional filtering
 * GET /api/products?category=watch - Filter by category
 * GET /api/products?search=rolex - Search products
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

require_once __DIR__ . '/../products.php';

try {
    $products = getProducts();
    
    // Get query parameters
    $category = isset($_GET['category']) ? $_GET['category'] : 'all';
    $searchQuery = isset($_GET['search']) ? strtolower($_GET['search']) : '';
    
    // Filter by category
    if ($category !== 'all') {
        $products = array_filter($products, function($product) use ($category) {
            return $product['category'] === $category;
        });
    }
    
    // Filter by search query
    if (!empty($searchQuery)) {
        $products = array_filter($products, function($product) use ($searchQuery) {
            return (
                stripos($product['name'], $searchQuery) !== false ||
                stripos($product['description'], $searchQuery) !== false
            );
        });
    }
    
    // Re-index array after filtering
    $products = array_values($products);
    
    $response = [
        'success' => true,
        'data' => $products,
        'count' => count($products)
    ];
    
    http_response_code(200);
    echo json_encode($response);
    
} catch (Exception $e) {
    error_log('Error fetching products: ' . $e->getMessage());
    $response = [
        'success' => false,
        'error' => 'Internal server error while fetching products'
    ];
    http_response_code(500);
    echo json_encode($response);
}
