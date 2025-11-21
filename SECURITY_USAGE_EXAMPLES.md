# Security Features Usage Examples

This document provides practical examples of how to use the security features implemented in the API.

## Table of Contents
1. [Authentication (JWT)](#authentication-jwt)
2. [Protected Endpoints](#protected-endpoints)
3. [Rate Limiting](#rate-limiting)
4. [Input Sanitization](#input-sanitization)
5. [Audit Logging](#audit-logging)
6. [Production Configuration](#production-configuration)

## Authentication (JWT)

### 1. Login to Get JWT Token

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer"
}
```

### 2. Save Token for Later Use

```bash
# Save token to variable
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"
```

### 3. Failed Login Attempt

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "wrongpassword"
  }'
```

**Response (401):**
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

## Protected Endpoints

### 1. Access Protected Endpoint WITH Token

```bash
curl http://localhost:5000/api/admin/products \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "data": [...],
  "count": 10,
  "user": "admin"
}
```

### 2. Access Protected Endpoint WITHOUT Token

```bash
curl http://localhost:5000/api/admin/products
```

**Response (401):**
```json
{
  "msg": "Missing Authorization Header"
}
```

### 3. Access Protected Endpoint with Invalid Token

```bash
curl http://localhost:5000/api/admin/products \
  -H "Authorization: Bearer invalid_token_here"
```

**Response (422):**
```json
{
  "msg": "Not enough segments"
}
```

## Rate Limiting

### 1. Normal API Usage (Within Limits)

```bash
# First request - success
curl http://localhost:5000/api/products

# Second request - success
curl http://localhost:5000/api/products

# ... up to 100 requests per minute
```

### 2. Exceeding Rate Limit

```bash
# After 100 requests in a minute
curl http://localhost:5000/api/products
```

**Response (429):**
```json
{
  "success": false,
  "error": "Rate limit exceeded. Please try again later."
}
```

### 3. Rate Limit on Login (Brute Force Prevention)

```bash
# Try 6 login attempts in 1 minute
for i in {1..6}; do
  curl -X POST http://localhost:5000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"wrong"}'
  echo ""
done
```

**After 5 attempts, response (429):**
```json
{
  "success": false,
  "error": "Rate limit exceeded. Please try again later."
}
```

## Input Sanitization

### 1. XSS Prevention in Search

```bash
# Try injecting script tag
curl "http://localhost:5000/api/products?search=<script>alert('xss')</script>"
```

**Response (200) - script tags removed:**
```json
{
  "success": true,
  "data": [],
  "count": 0
}
```

### 2. Category Validation

```bash
# Try invalid category
curl "http://localhost:5000/api/products?category=invalid<script>"
```

**Response (200) - defaults to 'all':**
```json
{
  "success": true,
  "data": [...],  // All 10 products
  "count": 10
}
```

### 3. Valid Categories

```bash
# Valid categories: all, watch, jewelry
curl "http://localhost:5000/api/products?category=watch"
```

**Response:**
```json
{
  "success": true,
  "data": [...],  // Only watches
  "count": 5
}
```

### 4. Long Password Prevention

```bash
# Try extremely long password (>200 chars)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"$(python3 -c 'print("a"*300)')\"}"
```

**Response (401) - rejected:**
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

## Audit Logging

### 1. View Audit Logs

```bash
# View last 20 audit log entries
tail -20 audit.log
```

**Example Output:**
```
2025-11-21 16:03:12 - audit - INFO - Action: HEALTH_CHECK | User: anonymous | Details: Health check performed | IP: 127.0.0.1
2025-11-21 16:03:15 - audit - INFO - Action: LOGIN_SUCCESS | User: admin | Details: User logged in: admin | IP: 127.0.0.1
2025-11-21 16:03:20 - audit - INFO - Action: GET_PRODUCTS | User: anonymous | Details: Category: all, Search: , Results: 10 | IP: 127.0.0.1
2025-11-21 16:03:25 - audit - INFO - Action: ADMIN_GET_PRODUCTS | User: admin | Details: Admin access | IP: 127.0.0.1
```

### 2. Monitor Failed Login Attempts

```bash
# Count failed login attempts
grep "LOGIN_FAILED" audit.log | wc -l

# Show recent failed logins
grep "LOGIN_FAILED" audit.log | tail -10
```

### 3. Monitor Rate Limit Violations

```bash
# Show rate limit violations
grep "RATE_LIMIT_EXCEEDED" audit.log
```

### 4. Monitor Admin Access

```bash
# Show admin endpoint access
grep "ADMIN_GET_PRODUCTS" audit.log
```

## Production Configuration

### 1. Set Environment Variables

```bash
# Generate secure JWT secret
export JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Enable production mode
export FLASK_ENV=production

# Optional: Set custom demo credentials
export DEMO_USERNAME=myadmin
export DEMO_PASSWORD=mysecurepassword123
```

### 2. Start Server in Production Mode

```bash
python backend/api.py
```

**Note:** In production mode:
- HTTPS is enforced
- JWT secret must be set (or app fails to start)
- CSP headers are enabled
- All security features are active

### 3. Production with Redis Rate Limiting

```python
# In backend/api.py, change:
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"  # Use Redis instead of memory
)
```

## Complete Workflow Example

### Scenario: Admin logs in and accesses protected data

```bash
#!/bin/bash

# 1. Check API health
echo "=== Checking API health ==="
curl -s http://localhost:5000/api/health | python3 -m json.tool

# 2. Login and get token
echo -e "\n=== Logging in ==="
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token obtained: ${TOKEN:0:20}..."

# 3. Access public endpoint
echo -e "\n=== Accessing public products endpoint ==="
curl -s http://localhost:5000/api/products | python3 -m json.tool | head -20

# 4. Access protected endpoint
echo -e "\n=== Accessing protected admin endpoint ==="
curl -s http://localhost:5000/api/admin/products \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -20

# 5. Check audit logs
echo -e "\n=== Recent audit logs ==="
tail -5 audit.log

echo -e "\n=== Workflow complete ==="
```

## Python Client Example

```python
import requests
import json

class SecureAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        """Login and store JWT token"""
        response = requests.post(
            f"{self.base_url}/api/auth/login",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['access_token']
            return True
        return False
    
    def get_products(self, category=None, search=None):
        """Get products with optional filters"""
        params = {}
        if category:
            params['category'] = category
        if search:
            params['search'] = search
        
        response = requests.get(
            f"{self.base_url}/api/products",
            params=params
        )
        return response.json()
    
    def get_admin_products(self):
        """Get products via protected admin endpoint"""
        if not self.token:
            raise Exception("Not authenticated. Call login() first.")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            f"{self.base_url}/api/admin/products",
            headers=headers
        )
        return response.json()

# Usage
client = SecureAPIClient()

# Login
if client.login("admin", "admin123"):
    print("✓ Login successful")
    
    # Get all products
    products = client.get_products()
    print(f"✓ Found {products['count']} products")
    
    # Search products
    watches = client.get_products(category="watch")
    print(f"✓ Found {watches['count']} watches")
    
    # Access protected endpoint
    admin_data = client.get_admin_products()
    print(f"✓ Admin access successful (user: {admin_data['user']})")
else:
    print("✗ Login failed")
```

## Security Testing

### Test Security Features

```bash
# Run all security tests
python -m pytest tests/test_api.py -v -k "security or auth or sanitization or login"

# Run specific security test
python -m pytest tests/test_api.py::test_login_success -v

# Run with coverage
python -m pytest tests/test_api.py --cov=backend --cov-report=html
```

## Troubleshooting

### Issue: "Missing Authorization Header"
**Solution:** Include Bearer token in Authorization header
```bash
curl http://localhost:5000/api/admin/products \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Issue: "Rate limit exceeded"
**Solution:** Wait for rate limit window to reset, or adjust limits in production

### Issue: JWT secret not set in production
**Solution:** 
```bash
export JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
```

### Issue: HTTPS not enforced
**Solution:** Set production environment:
```bash
export FLASK_ENV=production
```

## Additional Resources

- [SECURITY_FEATURES.md](SECURITY_FEATURES.md) - Complete security documentation
- [SECURITY.md](SECURITY.md) - Security policy
- [README.md](README.md) - General documentation

## Support

For security issues, see [SECURITY.md](SECURITY.md) for reporting procedures.
