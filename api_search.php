<?php
// Include products data
require_once 'products.php';

// Set JSON content type
header('Content-Type: application/json');

// Get search parameters
$query = isset($_GET['q']) ? strtolower($_GET['q']) : '';
$category = isset($_GET['category']) ? $_GET['category'] : 'all';

// Filter products
$filtered = $products;

if ($category !== 'all') {
    $filtered = array_filter($filtered, function($p) use ($category) {
        return $p['category'] === $category;
    });
}

if ($query !== '') {
    $filtered = array_filter($filtered, function($p) use ($query) {
        return strpos(strtolower($p['name']), $query) !== false ||
               strpos(strtolower($p['description']), $query) !== false;
    });
}

// Reset array keys and return as JSON
echo json_encode(array_values($filtered));
?>
