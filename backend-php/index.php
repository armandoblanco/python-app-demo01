<?php
/**
 * Main entry point for PHP backend
 * Simple router for API endpoints
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Get the request path
$requestUri = $_SERVER['REQUEST_URI'];
$scriptName = dirname($_SERVER['SCRIPT_NAME']);
$requestPath = str_replace($scriptName, '', $requestUri);

// Remove query string
$requestPath = strtok($requestPath, '?');

// Route to appropriate endpoint
if ($requestPath === '/api/health') {
    require __DIR__ . '/api/health.php';
} elseif ($requestPath === '/api/products') {
    require __DIR__ . '/api/products.php';
} elseif (preg_match('/^\/api\/products\/(\d+)$/', $requestPath, $matches)) {
    $_GET['id'] = $matches[1];
    require __DIR__ . '/api/product.php';
} elseif ($requestPath === '/api/categories') {
    require __DIR__ . '/api/categories.php';
} else {
    http_response_code(404);
    echo json_encode([
        'success' => false,
        'error' => 'Endpoint not found'
    ]);
}
