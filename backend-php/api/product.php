<?php
/**
 * Product by ID endpoint
 * GET /api/product.php?id=1 - Get specific product
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

require_once __DIR__ . '/../products.php';

try {
    $productId = isset($_GET['id']) ? intval($_GET['id']) : 0;
    
    if ($productId === 0) {
        $response = [
            'success' => false,
            'error' => 'Invalid product ID'
        ];
        http_response_code(400);
        echo json_encode($response);
        exit;
    }
    
    $products = getProducts();
    $product = null;
    
    foreach ($products as $p) {
        if ($p['id'] === $productId) {
            $product = $p;
            break;
        }
    }
    
    if ($product !== null) {
        $response = [
            'success' => true,
            'data' => $product
        ];
        http_response_code(200);
        echo json_encode($response);
    } else {
        $response = [
            'success' => false,
            'error' => 'Product not found'
        ];
        http_response_code(404);
        echo json_encode($response);
    }
    
} catch (Exception $e) {
    error_log('Error fetching product by ID: ' . $e->getMessage());
    $response = [
        'success' => false,
        'error' => 'Internal server error while fetching product'
    ];
    http_response_code(500);
    echo json_encode($response);
}
