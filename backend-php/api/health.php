<?php
/**
 * Health check endpoint
 * GET /api/health
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

$response = [
    'status' => 'healthy',
    'version' => '1.0.0'
];

http_response_code(200);
echo json_encode($response);
