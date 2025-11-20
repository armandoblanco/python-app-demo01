# PHP Backend API

This is the PHP implementation of the e-commerce backend API, providing RESTful endpoints for the luxury watches and jewelry catalog.

## Requirements

- PHP 7.4 or higher
- PHP extensions: curl, json, mbstring
- Composer (for dependency management and testing)
- Web server (Apache, Nginx, or PHP built-in server)

## Installation

1. Install Composer dependencies (for testing):
```bash
cd backend-php
composer install
```

## Running the Server

### Option 1: PHP Built-in Server (Development)

```bash
cd backend-php
php -S localhost:8080
```

The API will be available at: `http://localhost:8080`

### Option 2: Apache

1. Configure Apache to point to the `backend-php` directory
2. Ensure `.htaccess` is enabled (mod_rewrite)
3. The API will be available at your configured domain/path

### Option 3: Nginx

Configure Nginx with the following location block:

```nginx
location /api/ {
    try_files $uri $uri/ /index.php?$query_string;
}
```

## API Endpoints

All endpoints return JSON responses with CORS enabled.

### Health Check
```
GET /api/health.php
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Get All Products
```
GET /api/products.php
GET /api/products.php?category=watch
GET /api/products.php?search=rolex
GET /api/products.php?category=jewelry&search=diamante
```

Response:
```json
{
  "success": true,
  "data": [...],
  "count": 10
}
```

### Get Product by ID
```
GET /api/product.php?id=1
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Rolex Submariner",
    "category": "watch",
    "price": 12500.00,
    "description": "...",
    "image": "..."
  }
}
```

### Get Categories
```
GET /api/categories.php
```

Response:
```json
{
  "success": true,
  "data": [
    {"id": "all", "name": "Todos los Productos", "icon": "🏆"},
    {"id": "watch", "name": "Relojes de Lujo", "icon": "⌚"},
    {"id": "jewelry", "name": "Joyas Exclusivas", "icon": "💎"}
  ]
}
```

## Testing

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8080/api/health.php

# Get all products
curl http://localhost:8080/api/products.php

# Filter by category
curl http://localhost:8080/api/products.php?category=watch

# Search products
curl http://localhost:8080/api/products.php?search=rolex

# Get product by ID
curl http://localhost:8080/api/product.php?id=1

# Get categories
curl http://localhost:8080/api/categories.php
```

### Automated Tests with PHPUnit

```bash
# Install dependencies
composer install

# Run all tests
./vendor/bin/phpunit

# Run tests with verbose output
./vendor/bin/phpunit --verbose

# Run tests with coverage
./vendor/bin/phpunit --coverage-html coverage
```

## Project Structure

```
backend-php/
├── api/
│   ├── health.php          # Health check endpoint
│   ├── products.php        # Products list endpoint
│   ├── product.php         # Single product endpoint
│   └── categories.php      # Categories endpoint
├── tests/
│   └── ApiTest.php         # PHPUnit tests (13 tests)
├── products.php            # Product data and functions
├── index.php               # Main router (optional)
├── .htaccess              # Apache rewrite rules
├── composer.json          # Composer configuration
├── phpunit.xml            # PHPUnit configuration
└── README.md              # This file
```

## Error Handling

All endpoints include error handling:

- **404 Not Found**: Product or endpoint not found
- **500 Internal Server Error**: Server error with logged details
- **400 Bad Request**: Invalid parameters

Error response format:
```json
{
  "success": false,
  "error": "Error message"
}
```

## CORS Support

All endpoints include CORS headers to allow cross-origin requests from the frontend:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

## Security Considerations

1. Input validation on all parameters
2. Error logging without exposing sensitive details
3. Proper HTTP status codes
4. Type casting for IDs
5. SQL injection prevention (when using databases)

## Migration from Python/Flask

This PHP backend provides the same functionality as the Python Flask API:

- Same endpoint structure
- Same response format
- Same business logic
- Same CORS configuration
- Equivalent test coverage (13 tests)

See `PHP_MIGRATION.md` for detailed migration documentation.
