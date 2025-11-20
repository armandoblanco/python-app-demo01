<?php
/**
 * Categories endpoint
 * GET /api/categories - Get all available categories
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

require_once __DIR__ . '/../products.php';

try {
    $categories = getCategories();
    
    $response = [
        'success' => true,
        'data' => $categories
    ];
    
    http_response_code(200);
    echo json_encode($response);
    
} catch (Exception $e) {
    error_log('Error fetching categories: ' . $e->getMessage());
    $response = [
        'success' => false,
        'error' => 'Internal server error while fetching categories'
    ];
    http_response_code(500);
    echo json_encode($response);
}
