#!/bin/bash
# Simple test script for PHP backend API
# Tests all endpoints to ensure they work correctly

BASE_URL="http://localhost:8080"
PASSED=0
FAILED=0

echo "================================"
echo "PHP Backend API Tests"
echo "================================"
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
response=$(curl -s "$BASE_URL/api/health.php")
if echo "$response" | grep -q '"status":"healthy"'; then
    echo "✅ PASSED - Health check working"
    ((PASSED++))
else
    echo "❌ FAILED - Health check not working"
    ((FAILED++))
fi
echo ""

# Test 2: Get All Products
echo "Test 2: Get All Products"
response=$(curl -s "$BASE_URL/api/products.php")
count=$(echo "$response" | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ "$count" = "10" ]; then
    echo "✅ PASSED - All 10 products returned"
    ((PASSED++))
else
    echo "❌ FAILED - Expected 10 products, got $count"
    ((FAILED++))
fi
echo ""

# Test 3: Filter by Category (watch)
echo "Test 3: Filter by Category (watch)"
response=$(curl -s "$BASE_URL/api/products.php?category=watch")
count=$(echo "$response" | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ "$count" = "5" ]; then
    echo "✅ PASSED - 5 watches returned"
    ((PASSED++))
else
    echo "❌ FAILED - Expected 5 watches, got $count"
    ((FAILED++))
fi
echo ""

# Test 4: Filter by Category (jewelry)
echo "Test 4: Filter by Category (jewelry)"
response=$(curl -s "$BASE_URL/api/products.php?category=jewelry")
count=$(echo "$response" | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ "$count" = "5" ]; then
    echo "✅ PASSED - 5 jewelry items returned"
    ((PASSED++))
else
    echo "❌ FAILED - Expected 5 jewelry items, got $count"
    ((FAILED++))
fi
echo ""

# Test 5: Search Products
echo "Test 5: Search Products (rolex)"
response=$(curl -s "$BASE_URL/api/products.php?search=rolex")
if echo "$response" | grep -qi "rolex"; then
    echo "✅ PASSED - Search for 'rolex' working"
    ((PASSED++))
else
    echo "❌ FAILED - Search for 'rolex' not working"
    ((FAILED++))
fi
echo ""

# Test 6: Search with No Results
echo "Test 6: Search with No Results"
response=$(curl -s "$BASE_URL/api/products.php?search=nonexistent")
count=$(echo "$response" | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ "$count" = "0" ]; then
    echo "✅ PASSED - Empty search returns 0 results"
    ((PASSED++))
else
    echo "❌ FAILED - Expected 0 results, got $count"
    ((FAILED++))
fi
echo ""

# Test 7: Combined Search and Filter
echo "Test 7: Combined Search and Filter (category=watch, search=omega)"
response=$(curl -s "$BASE_URL/api/products.php?category=watch&search=omega")
if echo "$response" | grep -qi "omega"; then
    echo "✅ PASSED - Combined filter working"
    ((PASSED++))
else
    echo "❌ FAILED - Combined filter not working"
    ((FAILED++))
fi
echo ""

# Test 8: Get Product by ID
echo "Test 8: Get Product by ID (id=1)"
response=$(curl -s "$BASE_URL/api/product.php?id=1")
if echo "$response" | grep -q '"id":1'; then
    echo "✅ PASSED - Get product by ID working"
    ((PASSED++))
else
    echo "❌ FAILED - Get product by ID not working"
    ((FAILED++))
fi
echo ""

# Test 9: Product Not Found
echo "Test 9: Product Not Found (id=999)"
response=$(curl -s "$BASE_URL/api/product.php?id=999")
status_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/product.php?id=999")
if [ "$status_code" = "404" ]; then
    echo "✅ PASSED - 404 error for non-existent product"
    ((PASSED++))
else
    echo "❌ FAILED - Expected 404, got $status_code"
    ((FAILED++))
fi
echo ""

# Test 10: Get Categories
echo "Test 10: Get Categories"
response=$(curl -s "$BASE_URL/api/categories.php")
if echo "$response" | grep -q "Relojes de Lujo" && echo "$response" | grep -q "Joyas Exclusivas"; then
    echo "✅ PASSED - Categories endpoint working"
    ((PASSED++))
else
    echo "❌ FAILED - Categories endpoint not working"
    ((FAILED++))
fi
echo ""

# Test 11: Products Have Required Fields
echo "Test 11: Products Have Required Fields"
response=$(curl -s "$BASE_URL/api/products.php")
if echo "$response" | grep -q '"id":' && \
   echo "$response" | grep -q '"name":' && \
   echo "$response" | grep -q '"category":' && \
   echo "$response" | grep -q '"price":' && \
   echo "$response" | grep -q '"description":' && \
   echo "$response" | grep -q '"image":'; then
    echo "✅ PASSED - All required fields present"
    ((PASSED++))
else
    echo "❌ FAILED - Missing required fields"
    ((FAILED++))
fi
echo ""

# Test 12: Product Prices Are Valid
echo "Test 12: Product Prices Are Valid"
response=$(curl -s "$BASE_URL/api/products.php")
if echo "$response" | grep -q '"price":[0-9]\+'; then
    echo "✅ PASSED - Product prices are valid numbers"
    ((PASSED++))
else
    echo "❌ FAILED - Product prices are not valid"
    ((FAILED++))
fi
echo ""

# Test 13: CORS Headers
echo "Test 13: CORS Headers"
headers=$(curl -s -I "$BASE_URL/api/health.php")
if echo "$headers" | grep -qi "Access-Control-Allow-Origin"; then
    echo "✅ PASSED - CORS headers present"
    ((PASSED++))
else
    echo "❌ FAILED - CORS headers missing"
    ((FAILED++))
fi
echo ""

# Summary
echo "================================"
echo "Test Summary"
echo "================================"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Total: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✅ ALL TESTS PASSED!"
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    exit 1
fi
